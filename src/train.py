"""Reproducible training: fit TF-IDF inside CV and reserve the test split."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import joblib
import pandas as pd
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, make_scorer, recall_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from src.preprocessing import clean_text

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / 'models'
CLASS_NAMES = ['Normal', 'Penipuan', 'Promosi']
SEED = 42
MODEL_FILES = {
    'Multinomial Naive Bayes': 'multinomial_naive_bayes_id.joblib',
    'Logistic Regression': 'logistic_regression_id.joblib',
    'Linear SVM': 'linear_svm_id.joblib',
}

def fingerprint(path: Path) -> str:
    # Git may convert CRLF to LF on Cloud; source fingerprints are newline-neutral.
    data = path.read_text(encoding='utf-8-sig').encode('utf-8') if path.suffix in {'.py', '.csv'} else path.read_bytes()
    return hashlib.sha256(data).hexdigest()

def prepare_data(lang: str) -> pd.DataFrame:
    path = ROOT / ('Indonesia/dataset_indonesia_standard.csv' if lang == 'id'
                   else 'Inggris/dataset_inggris_standard.csv')
    frame = pd.read_csv(path).dropna(subset=['text', 'label_3class']).copy()
    if lang == 'en':
        # Broad categories do not identify a unique three-class label.
        frame = frame[frame['sub_category'].isin(
            ['normal', 'phishing', 'job_scam', 'scam', 'marketing', 'promo'])].copy()
    frame['cleaned_text'] = frame['text'].map(lambda text: clean_text(text, lang=lang))
    frame = frame[frame['cleaned_text'].str.len() > 0]
    return frame.drop_duplicates('cleaned_text').reset_index(drop=True)

def split_data(frame):
    return train_test_split(frame, test_size=0.2, random_state=SEED,
                            stratify=frame['label_3class'])

def metrics(y_true, y_pred) -> dict:
    report = classification_report(y_true, y_pred, labels=[0, 1, 2],
                                   target_names=CLASS_NAMES, output_dict=True, zero_division=0)
    return {
        'accuracy': round(float(report['accuracy']), 4),
        'precision_macro': round(float(report['macro avg']['precision']), 4),
        'recall_macro': round(float(report['macro avg']['recall']), 4),
        'f1_macro': round(float(report['macro avg']['f1-score']), 4),
        'per_class': {name: {
            'precision': round(float(report[name]['precision']), 4),
            'recall': round(float(report[name]['recall']), 4),
            'f1': round(float(report[name]['f1-score']), 4),
            'support': int(report[name]['support']),
        } for name in CLASS_NAMES},
        'confusion_matrix': confusion_matrix(y_true, y_pred, labels=[0, 1, 2]).tolist(),
    }

def pipeline(classifier, min_df=2):
    return Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=min_df, sublinear_tf=True)),
        ('classifier', classifier),
    ])

def train_and_evaluate_indonesian():
    frame = prepare_data('id')
    train, test = split_data(frame)
    candidates = {
        'Multinomial Naive Bayes': pipeline(MultinomialNB(alpha=0.3)),
        'Logistic Regression': pipeline(LogisticRegression(
            C=2.5, class_weight='balanced', max_iter=1000, random_state=SEED)),
        'Linear SVM': pipeline(CalibratedClassifierCV(LinearSVC(
            C=1.0, class_weight='balanced', random_state=SEED))),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    scoring = {'f1_macro': 'f1_macro', 'recall_penipuan': make_scorer(
        recall_score, labels=[1], average='macro', zero_division=0)}
    results, selection_scores = [], {}
    for name, model in candidates.items():
        scores = cross_validate(model, train['cleaned_text'], train['label_3class'],
                                cv=cv, scoring=scoring)
        f1 = float(scores['test_f1_macro'].mean())
        fraud_recall = float(scores['test_recall_penipuan'].mean())
        selection_scores[name] = (f1, fraud_recall)
        results.append({'model_name': name,
                        'cv_f1_macro_mean': round(f1, 4),
                        'cv_f1_macro_std': round(float(scores['test_f1_macro'].std()), 4),
                        'cv_recall_penipuan_mean': round(fraud_recall, 4)})
        print(f'{name}: CV macro-F1 = {f1:.4f}', flush=True)
    # Choose before inspecting any test result.
    selected = max(selection_scores, key=selection_scores.get)
    for result in results:
        name = result['model_name']
        model = candidates[name]
        model.fit(train['cleaned_text'], train['label_3class'])
        result['train'] = metrics(train['label_3class'], model.predict(train['cleaned_text']))
        result['test'] = metrics(test['label_3class'], model.predict(test['cleaned_text']))
        joblib.dump(model, MODELS / MODEL_FILES[name])
    best = candidates[selected]
    joblib.dump(best, MODELS / 'best_model_id.joblib')
    joblib.dump(best.named_steps['tfidf'], MODELS / 'tfidf_vectorizer_id.joblib')
    rows = []
    for result in results:
        row = {key: value for key, value in result.items() if key not in {'train', 'test'}}
        row.update({key: value for key, value in result['test'].items()
                    if key not in {'per_class', 'confusion_matrix'}})
        row['recall_penipuan'] = result['test']['per_class']['Penipuan']['recall']
        rows.append(row)
    pd.DataFrame(rows).to_csv(MODELS / 'model_comparison_id.csv', index=False)
    (MODELS / 'model_comparison_id.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    return {'selected_model': selected,
            'selection_rule': 'Highest mean 5-fold CV macro-F1 on training data; fraud recall breaks ties.',
            'dataset_rows': len(frame), 'train_rows': len(train), 'test_rows': len(test),
            'class_distribution': {CLASS_NAMES[int(k)]: int(v) for k, v in
                                   frame['label_3class'].value_counts().items()},
            'models': results}

def train_english_model():
    frame = prepare_data('en')
    train, test = split_data(frame)
    model = pipeline(LogisticRegression(C=2.0, class_weight='balanced',
                                       max_iter=1000, random_state=SEED), min_df=3)
    model.fit(train['cleaned_text'], train['label_3class'])
    joblib.dump(model, MODELS / 'best_model_en.joblib')
    joblib.dump(model.named_steps['tfidf'], MODELS / 'tfidf_vectorizer_en.joblib')
    result = {'model_name': 'Logistic Regression', 'dataset_rows': len(frame),
              'train_rows': len(train), 'test_rows': len(test),
              'test': metrics(test['label_3class'], model.predict(test['cleaned_text'])),
              'note': 'English source provenance needs independent validation; results are exploratory.'}
    print(f"English: {len(frame)} messages, accuracy = {result['test']['accuracy']:.4f}", flush=True)
    return result

def main():
    MODELS.mkdir(exist_ok=True)
    evaluation = {
        'schema_version': 3, 'random_seed': SEED,
        'scikit_learn_version': sklearn.__version__,
        'source_sha256': {
            'indonesia_csv': fingerprint(ROOT / 'Indonesia/dataset_indonesia_standard.csv'),
            'english_csv': fingerprint(ROOT / 'Inggris/dataset_inggris_standard.csv'),
            'preprocessing_py': fingerprint(ROOT / 'src/preprocessing.py'),
        },
        'indonesian': train_and_evaluate_indonesian(),
        'english': train_english_model(),
    }
    evaluation['artifact_sha256'] = {
        name: fingerprint(MODELS / name)
        for name in [*MODEL_FILES.values(), 'best_model_id.joblib', 'best_model_en.joblib']}
    (MODELS / 'evaluation.json').write_text(json.dumps(evaluation, indent=2), encoding='utf-8')
    print(f"Selected: {evaluation['indonesian']['selected_model']}", flush=True)

if __name__ == '__main__':
    main()
