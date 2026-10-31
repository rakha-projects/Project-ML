"""
Skrip Pelatihan Model Machine Learning, Hyperparameter Tuning & Evaluasi Komprehensif.
Membandingkan 3 Algoritma: Multinomial Naive Bayes, Logistic Regression, dan Linear SVM.
Mengekspor model dan vectorizer ke folder Project/models/ untuk digunakan di Streamlit.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_INDO = os.path.join(BASE_DIR, "Indonesia", "dataset_indonesia_standard.csv")
DATASET_ENG = os.path.join(BASE_DIR, "Inggris", "dataset_inggris_standard.csv")

MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

RESULTS_DIR = os.path.join(BASE_DIR, "eda_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

CLASS_NAMES = ["Normal", "Penipuan", "Promosi"]

def train_and_evaluate_indonesian():
    print("=" * 70)
    print("PELATIHAN & EVALUASI MODEL BAHASA INDONESIA (3 KELAS)")
    print("=" * 70)

    # 1. Muat Dataset Bersih Terstandarisasi
    df = pd.read_csv(DATASET_INDO)
    X = df["cleaned_text"].astype(str)
    y = df["label_3class"].astype(int)

    print(f"[*] Total dataset: {len(df)} sampel")
    print(f"    - Normal (0)   : {sum(y == 0)} ({sum(y == 0)/len(y)*100:.1f}%)")
    print(f"    - Penipuan (1) : {sum(y == 1)} ({sum(y == 1)/len(y)*100:.1f}%)")
    print(f"    - Promosi (2)  : {sum(y == 2)} ({sum(y == 2)/len(y)*100:.1f}%)")

    # 2. Stratified Train-Test Split (80% Train : 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[*] Pembagian data: Train = {len(X_train)} sampel | Test = {len(X_test)} sampel")

    # 3. TF-IDF Vectorizer (Hanya di-fit pada data latih untuk mencegah Data Leakage)
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"[*] Kosakata TF-IDF terbentuk: {X_train_vec.shape[1]} fitur n-gram")

    # Simpan Vectorizer
    vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer_id.joblib")
    joblib.dump(vectorizer, vec_path)
    print(f"[V] Vectorizer tersimpan di: {vec_path}")

    # 4. Definisikan 3 Algoritma Pembanding
    # Menggunakan CalibratedClassifierCV pada LinearSVC agar menghasilkan predict_proba() untuk Streamlit
    models = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.3),
        "Logistic Regression": LogisticRegression(C=2.5, class_weight="balanced", max_iter=1000, random_state=42),
        "Linear SVM": CalibratedClassifierCV(LinearSVC(C=1.0, class_weight="balanced", random_state=42))
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    comparison_results = []
    confusion_matrices = {}

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, (name, clf) in enumerate(models.items()):
        print(f"\n---> Memproses Model {idx+1}: {name}")
        
        # Validasi Silang (5-Fold CV pada Data Latih)
        cv_scores = cross_val_score(clf, X_train_vec, y_train, cv=cv, scoring="f1_macro")
        print(f"     5-Fold CV Macro-F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        # Training pada keseluruhan Data Latih
        clf.fit(X_train_vec, y_train)

        # Evaluasi pada Data Uji Independen (Test Set)
        y_pred = clf.predict(X_test_vec)

        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)

        # Metrik spesifik per-kelas
        prec_per_class = precision_score(y_test, y_pred, average=None, zero_division=0)
        rec_per_class = recall_score(y_test, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        confusion_matrices[name] = cm.tolist()

        # Visualisasi Confusion Matrix Heatmap
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[idx],
                    xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
        axes[idx].set_title(f"{name}\nAcc: {acc*100:.2f}% | F1: {f1_macro*100:.2f}%", weight="bold")
        axes[idx].set_xlabel("Prediksi Model")
        axes[idx].set_ylabel("Aktual (Ground Truth)")

        # Simpan Model Terlatih
        safe_name = name.lower().replace(" ", "_")
        model_save_path = os.path.join(MODELS_DIR, f"{safe_name}_id.joblib")
        joblib.dump(clf, model_save_path)
        print(f"     Model disimpan di: {model_save_path}")

        res = {
            "model_name": name,
            "accuracy": round(float(acc), 4),
            "precision_macro": round(float(prec_macro), 4),
            "recall_macro": round(float(rec_macro), 4),
            "f1_macro": round(float(f1_macro), 4),
            "cv_f1_macro_mean": round(float(cv_scores.mean()), 4),
            "cv_f1_macro_std": round(float(cv_scores.std()), 4),
            "recall_normal": round(float(rec_per_class[0]), 4),
            "recall_penipuan": round(float(rec_per_class[1]), 4),
            "recall_promosi": round(float(rec_per_class[2]), 4),
            "f1_normal": round(float(f1_per_class[0]), 4),
            "f1_penipuan": round(float(f1_per_class[1]), 4),
            "f1_promosi": round(float(f1_per_class[2]), 4)
        }
        comparison_results.append(res)

    plt.tight_layout()
    cm_path = os.path.join(RESULTS_DIR, "confusion_matrices.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"\n[V] Visualisasi Confusion Matrix tersimpan di: {cm_path}")

    # Simpan Hasil Perbandingan Model ke JSON & CSV
    comp_df = pd.DataFrame(comparison_results)
    comp_csv_path = os.path.join(MODELS_DIR, "model_comparison_id.csv")
    comp_json_path = os.path.join(MODELS_DIR, "model_comparison_id.json")
    comp_df.to_csv(comp_csv_path, index=False)
    with open(comp_json_path, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=4)
    print(f"[V] Tabel perbandingan tersimpan di: {comp_csv_path}")

    # Tentukan Model Terbaik berdasarkan Macro-F1 dan Recall Penipuan
    # Sorting: Prioritas Macro-F1, kemudian Recall Penipuan
    best_res = sorted(comparison_results, key=lambda x: (x["f1_macro"], x["recall_penipuan"]), reverse=True)[0]
    best_model_name = best_res["model_name"]
    best_safe_name = best_model_name.lower().replace(" ", "_")
    best_model_obj = joblib.load(os.path.join(MODELS_DIR, f"{best_safe_name}_id.joblib"))
    
    # Simpan pointer model terbaik
    joblib.dump(best_model_obj, os.path.join(MODELS_DIR, "best_model_id.joblib"))
    print(f"\n[*] MODEL TERBAIK INDONESIA: {best_model_name}")
    print(f"    Accuracy       : {best_res['accuracy']*100:.2f}%")
    print(f"    Macro F1-Score : {best_res['f1_macro']*100:.2f}%")
    print(f"    Recall Penipuan: {best_res['recall_penipuan']*100:.2f}%")

    return comp_df, best_model_name


def train_english_model():
    print("\n" + "=" * 70)
    print("PELATIHAN MODEL BAHASA INGGRIS (UNTUK FITUR MULTILINGUAL WEB)")
    print("=" * 70)

    df_eng = pd.read_csv(DATASET_ENG)
    df_eng = df_eng.dropna(subset=["cleaned_text"])
    df_eng = df_eng[df_eng["cleaned_text"].str.strip() != ""]
    
    X = df_eng["cleaned_text"].astype(str)
    y = df_eng["label_3class"].astype(int)

    # 80:20 Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    vec_en = TfidfVectorizer(ngram_range=(1, 2), min_df=3, sublinear_tf=True)
    X_train_vec = vec_en.fit_transform(X_train)
    X_test_vec = vec_en.transform(X_test)

    # Latih Logistic Regression untuk bahasa Inggris
    clf_en = LogisticRegression(C=2.0, class_weight="balanced", max_iter=1000, random_state=42)
    clf_en.fit(X_train_vec, y_train)

    y_pred = clf_en.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")

    print(f"[*] Model Inggris (Logistic Regression) Terlatih!")
    print(f"    Akurasi: {acc*100:.2f}% | Macro F1-Score: {f1*100:.2f}%")

    # Simpan artefak model Inggris
    joblib.dump(vec_en, os.path.join(MODELS_DIR, "tfidf_vectorizer_en.joblib"))
    joblib.dump(clf_en, os.path.join(MODELS_DIR, "best_model_en.joblib"))
    print(f"[V] Artefak model Inggris berhasil disimpan di {MODELS_DIR}")


if __name__ == "__main__":
    comp_df, best_name = train_and_evaluate_indonesian()
    train_english_model()

    print("\n" + "=" * 70)
    print("MILESTONE 4 SELESAI DENGAN SUKSES!")
    print("=" * 70)
