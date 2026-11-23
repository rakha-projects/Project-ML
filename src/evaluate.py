"""Generate evaluation figures, error analysis and a report from current artifacts."""
from __future__ import annotations
import json
from pathlib import Path
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from src.inference import linear_coefficients
from src.train import CLASS_NAMES, MODEL_FILES, MODELS, ROOT, fingerprint, metrics, prepare_data, split_data


def run_evaluation():
    evaluation = json.loads((MODELS / 'evaluation.json').read_text(encoding='utf-8'))
    if evaluation['source_sha256']['preprocessing_py'] != fingerprint(ROOT / 'src/preprocessing.py'):
        raise ValueError('Preprocessing changed. Run python -m src.train first.')
    train, test = split_data(prepare_data('id'))
    plots = ROOT / 'eda_results'
    plots.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for ax, result in zip(axes, evaluation['indonesian']['models']):
        model = joblib.load(MODELS / MODEL_FILES[result['model_name']])
        actual = metrics(test['label_3class'], model.predict(test['cleaned_text']))
        if actual != result['test']:
            raise ValueError('Evaluation does not match model artifacts. Run python -m src.train.')
        sns.heatmap(actual['confusion_matrix'], annot=True, fmt='d', cmap='Greens', ax=ax,
                    xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar=False)
        ax.set_title(result['model_name'])
        ax.set_xlabel('Prediksi')
        ax.set_ylabel('Aktual')
    fig.tight_layout()
    fig.savefig(plots / 'confusion_matrices.png', dpi=200)
    plt.close(fig)
    best_name = evaluation['indonesian']['selected_model']
    best = joblib.load(MODELS / 'best_model_id.joblib')
    predictions = best.predict(test['cleaned_text'])
    errors = pd.DataFrame({
        'Teks_SMS': test['text'],
        'Kategori_Aktual': test['label_3class'].map(dict(enumerate(CLASS_NAMES))),
        'Prediksi_Model': [CLASS_NAMES[int(label)] for label in predictions],
    })
    errors = errors[errors['Kategori_Aktual'] != errors['Prediksi_Model']]
    errors.to_csv(MODELS / 'error_analysis.csv', index=False)
    weights, approximate = linear_coefficients(best.named_steps['classifier'])
    if weights is not None:
        features = best.named_steps['tfidf'].get_feature_names_out()
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        for i, (ax, label) in enumerate(zip(axes, CLASS_NAMES)):
            indexes = np.argsort(weights[i])[-12:]
            ax.barh(features[indexes], weights[i][indexes], color=['#236447', '#b13b3b', '#a77021'][i])
            ax.set_title(label)
            ax.set_xlabel('Rata-rata bobot linear' if approximate else 'Bobot linear')
        fig.suptitle(f'Fitur model terpilih: {best_name}')
        fig.tight_layout()
        fig.savefig(plots / 'feature_importance.png', dpi=200)
        plt.close(fig)
    def pct(value):
        return f'{value * 100:.2f}%'
    lines = [
        '# Evaluasi Model SmishingGuard', '',
        'Laporan ini dihasilkan oleh `python -m src.evaluate` dari artefak dan `models/evaluation.json` saat ini.', '',
        '## Metodologi', '',
        f"Dataset Indonesia: {evaluation['indonesian']['dataset_rows']} SMS unik; {len(train)} latih dan {len(test)} uji, stratified split 80:20, seed 42.",
        'Teks mentah dibersihkan menggunakan fungsi yang sama dengan aplikasi. TF-IDF unigram dan bigram dipelajari di dalam setiap fold CV. Model dipilih dari mean macro-F1 5-fold CV data latih; recall Penipuan menjadi pemecah seri. Data uji dinilai sesudah pemilihan.', '',
        f'**Model terpilih: {best_name}.**', '',
        '## Perbandingan model', '',
        '| Algoritma | CV Macro-F1 | Akurasi uji | Precision macro | Recall macro | Macro-F1 uji | Recall Penipuan |',
        '|---|---:|---:|---:|---:|---:|---:|',
    ]
    for result in evaluation['indonesian']['models']:
        t = result['test']
        lines.append(f"| {result['model_name']} | {result['cv_f1_macro_mean']:.4f} ± {result['cv_f1_macro_std']:.4f} | {pct(t['accuracy'])} | {pct(t['precision_macro'])} | {pct(t['recall_macro'])} | {pct(t['f1_macro'])} | {pct(t['per_class']['Penipuan']['recall'])} |")
    lines += ['', '## Generalisasi', '', '| Model | Macro-F1 latih | Macro-F1 uji | Selisih (poin persentase) |', '|---|---:|---:|---:|']
    for result in evaluation['indonesian']['models']:
        lines.append(f"| {result['model_name']} | {pct(result['train']['f1_macro'])} | {pct(result['test']['f1_macro'])} | {(result['train']['f1_macro']-result['test']['f1_macro'])*100:.2f} |")
    lines += ['', 'Selisih latih-uji pada satu split belum membuktikan tidak adanya overfitting. Belum ada uji eksternal pada SMS Indonesia terbaru.', '',
              '## Analisis kesalahan', '', f'{len(errors)} kesalahan dari {len(test)} SMS uji pada model {best_name}.', '',
              'Rincian teks dan label tersedia di `models/error_analysis.csv`; tabel interaktif ada di dashboard aplikasi.', '',
              '![Confusion matrix](eda_results/confusion_matrices.png)', '',
              '![Fitur berpengaruh](eda_results/feature_importance.png)', '',
              'Bobot SVM terkalibrasi dirata-ratakan dari estimator kalibrasi. Kontribusi kata merupakan perkiraan linear, bukan penjelasan kausal.', '',
              '## Model Inggris', '',
              f"{evaluation['english']['dataset_rows']} pesan unik dari kategori asal yang lebih jelas, dengan {evaluation['english']['train_rows']} data latih dan {evaluation['english']['test_rows']} data uji. Akurasi {pct(evaluation['english']['test']['accuracy'])}; macro-F1 {pct(evaluation['english']['test']['f1_macro'])}.",
              'Kategori umum seperti spam, adult, crypto, dan giveaway tidak digunakan untuk training. Asal korpus masih perlu verifikasi independen; hasil ini bersifat eksploratif.', '',
              '## Keterbatasan', '',
              '- Data Indonesia relatif kecil dan lama; anotasi dataset dapat ambigu.',
              '- Kosakata baru, bahasa campuran, dan ejaan tersamarkan dapat menghasilkan prediksi yang keliru.',
              '- Deteksi bahasa memakai aturan kata; pilihan manual tersedia.',
              '- Skor kelas Penipuan bukan skor keamanan terverifikasi. Aplikasi tidak membuka URL atau mengesahkan pengirim.',
              '- Indikator heuristik terpisah dari probabilitas model dan tidak mengubah label prediksi.', '',
              f"Versi scikit-learn artefak: {evaluation['scikit_learn_version']}. Hash sumber dan artefak tercantum pada `models/evaluation.json`."]
    (ROOT / 'Evaluation_Report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Evaluated {best_name}: {len(errors)} errors / {len(test)} test messages.')


if __name__ == '__main__':
    run_evaluation()
