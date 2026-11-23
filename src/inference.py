"""Prediction helpers shared by the single SMS and CSV views."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.preprocessing import clean_text, detect_language, extract_heuristic_features

LABELS = {0: "Normal", 1: "Penipuan", 2: "Promosi"}
MAX_SMS_CHARS = 2000
RESULT_COLUMNS = (
    "Prediksi_Kategori", "Keyakinan_Model_%", "Skor_Penipuan_Model_%",
    "Skor_Heuristik_Terpisah", "Bahasa_Model", "Status_Risiko", "Status",
)


def linear_coefficients(classifier):
    """Return linear weights; calibrated SVM weights are an ensemble average."""
    if hasattr(classifier, "coef_"):
        return classifier.coef_, False
    estimators = getattr(classifier, "calibrated_classifiers_", [])
    coefficients = [
        item.estimator.coef_
        for item in estimators
        if hasattr(item.estimator, "coef_")
    ]
    if coefficients:
        return np.mean(coefficients, axis=0), True
    return None, False


def analyze_sms(text: str, language_mode: str, pipelines: dict[str, Any]) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Isi SMS masih kosong.")
    if len(text) > MAX_SMS_CHARS:
        raise ValueError(f"Pesan terlalu panjang. Batasnya {MAX_SMS_CHARS} karakter.")
    if language_mode not in {"auto", "id", "en"}:
        raise ValueError("Pilihan bahasa tidak dikenal.")

    detected = detect_language(text)
    lang = detected["language"] if language_mode == "auto" else language_mode
    cleaned = clean_text(text, lang=lang)
    if not cleaned:
        raise ValueError("Pesan tidak memiliki kata yang dapat dianalisis.")

    pipeline = pipelines[lang]
    vectorizer = pipeline.named_steps["tfidf"]
    features = vectorizer.transform([cleaned])
    # A prediction with no known vocabulary is especially unreliable.
    no_known_terms = features.nnz == 0
    classifier = pipeline.named_steps["classifier"]
    proba = classifier.predict_proba(features)[0]
    predicted_id = int(classifier.classes_[np.argmax(proba)])
    probabilities = {
        LABELS[int(class_id)]: float(probability)
        for class_id, probability in zip(classifier.classes_, proba)
    }

    contributions = []
    coefficients, approximate = linear_coefficients(classifier)
    if coefficients is not None:
        class_index = list(classifier.classes_).index(predicted_id)
        weighted = features.multiply(coefficients[class_index]).toarray().ravel()
        terms = vectorizer.get_feature_names_out()
        for index in np.argsort(weighted)[-5:][::-1]:
            if weighted[index] > 0:
                contributions.append({"term": str(terms[index]), "contribution": float(weighted[index])})

    return {
        "label": LABELS[predicted_id],
        "language": lang,
        "language_detected": detected["language"],
        "language_score": detected["confidence"],
        "language_ambiguous": (
            detected["id_score"] + detected["en_score"] < 2
            or detected["confidence"] <= 0.6
        ),
        "probabilities": probabilities,
        "fraud_score": probabilities.get("Penipuan", 0.0) * 100,
        "cleaned_text": cleaned,
        "heuristics": extract_heuristic_features(text, lang=lang),
        "contributions": contributions,
        "contributions_approximate": approximate,
        "no_known_terms": no_known_terms,
    }


def analyze_batch(frame, column: str, language_mode: str, pipelines: dict[str, Any]):
    """Return a copy of a CSV frame with results for every valid SMS row."""
    if column not in frame.columns:
        raise ValueError("Kolom teks tidak ditemukan pada CSV.")
    output = frame.copy()
    # Preserve uploaded columns even when re-importing a previous results CSV.
    used = set(output.columns)
    rename = {}
    for name in RESULT_COLUMNS:
        if name in used:
            target = name + "_Input"
            while target in used:
                target += "_Input"
            used.add(target)
            rename[name] = target
    output = output.rename(columns=rename)
    labels, fraud_scores, confidences, heuristic_scores = [], [], [], []
    languages, risk_statuses, statuses = [], [], []
    for value in frame[column]:
        try:
            row = analyze_sms(value, language_mode, pipelines)
            labels.append(row["label"])
            fraud_scores.append(round(row["fraud_score"], 2))
            confidences.append(round(row["probabilities"][row["label"]] * 100, 2))
            heuristic_scores.append(row["heuristics"]["heuristic_risk_score"])
            languages.append(row["language"])
            risk_statuses.append("Periksa lebih lanjut" if row["label"] == "Penipuan" else "Belum terverifikasi")
            statuses.append("Perlu tinjauan" if row["no_known_terms"] else "Terproses")
        except ValueError as exc:
            labels.append("")
            fraud_scores.append(None)
            confidences.append(None)
            heuristic_scores.append(None)
            languages.append("")
            risk_statuses.append("")
            statuses.append(str(exc))
    output["Prediksi_Kategori"] = labels
    output["Keyakinan_Model_%"] = confidences
    output["Skor_Penipuan_Model_%"] = fraud_scores
    output["Skor_Heuristik_Terpisah"] = heuristic_scores
    output["Bahasa_Model"] = languages
    output["Status_Risiko"] = risk_statuses
    output["Status"] = statuses
    return output


def safe_csv_bytes(frame) -> bytes:
    """Prevent spreadsheet programs from executing formulas in exported SMS text."""
    export = frame.copy()
    def neutralize(value):
        return "'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value

    for column in export.select_dtypes(include=["object", "string"]).columns:
        export[column] = export[column].map(neutralize)
    export.columns = [neutralize(column) for column in export.columns]
    return export.to_csv(index=False).encode("utf-8-sig")
