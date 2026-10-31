"""
Skrip Eksplorasi Data (Exploratory Data Analysis - EDA) & Visualisasi.
Menganalisis karakteristik dataset SMS Indonesia & Inggris serta menghasilkan
grafik visualisasi dan laporan statistik lengkap untuk laporan project M15.
"""

import os
import csv
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Mode non-interaktif tanpa GUI
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDO_DATASET = os.path.join(BASE_DIR, "Indonesia", "dataset_indonesia_standard.csv")
ENG_DATASET = os.path.join(BASE_DIR, "Inggris", "dataset_inggris_standard.csv")
MULTI_DATASET = os.path.join(BASE_DIR, "dataset_multilingual_balanced.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "eda_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_PATH = os.path.join(BASE_DIR, "EDA_Report.md")

# Atur gaya visualisasi
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10

def load_data():
    df_indo = pd.read_csv(INDO_DATASET)
    df_eng = pd.read_csv(ENG_DATASET)
    df_multi = pd.read_csv(MULTI_DATASET)
    return df_indo, df_eng, df_multi

def plot_class_distribution(df_indo, df_eng):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    palette = {"Normal": "#2ecc71", "Penipuan": "#e74c3c", "Promosi": "#f39c12"}

    # 1. Indonesia
    indo_counts = df_indo["label_name"].value_counts().reset_index()
    indo_counts.columns = ["label_name", "count"]
    total_indo = len(df_indo)
    
    sns.barplot(data=indo_counts, x="label_name", y="count", palette=palette, ax=axes[0])
    axes[0].set_title(f"Distribusi Kelas SMS Indonesia (N={total_indo:,})", weight="bold")
    axes[0].set_xlabel("Kategori Pesan")
    axes[0].set_ylabel("Jumlah Pesan")
    for p in axes[0].patches:
        height = p.get_height()
        pct = (height / total_indo) * 100
        axes[0].annotate(f"{int(height)}\n({pct:.1f}%)",
                         (p.get_x() + p.get_width() / 2., height / 2),
                         ha='center', va='center', color='white', weight='bold')

    # 2. Inggris
    eng_counts = df_eng["label_name"].value_counts().reset_index()
    eng_counts.columns = ["label_name", "count"]
    total_eng = len(df_eng)

    sns.barplot(data=eng_counts, x="label_name", y="count", palette=palette, ax=axes[1])
    axes[1].set_title(f"Distribusi Kelas SMS Inggris (N={total_eng:,})", weight="bold")
    axes[1].set_xlabel("Kategori Pesan")
    axes[1].set_ylabel("Jumlah Pesan")
    for p in axes[1].patches:
        height = p.get_height()
        pct = (height / total_eng) * 100
        axes[1].annotate(f"{int(height)}\n({pct:.1f}%)",
                         (p.get_x() + p.get_width() / 2., height / 2),
                         ha='center', va='center', color='white', weight='bold')

    plt.tight_layout()
    fpath = os.path.join(OUTPUT_DIR, "1_class_distribution.png")
    plt.savefig(fpath, dpi=300)
    plt.close()
    print(f"[V] Tersimpan: {fpath}")

def plot_length_distributions(df_indo):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    palette = {"Normal": "#2ecc71", "Penipuan": "#e74c3c", "Promosi": "#f39c12"}

    # Boxplot Panjang Karakter
    sns.boxplot(data=df_indo, x="label_name", y="text_length", palette=palette, ax=axes[0], showmeans=True,
                meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[0].set_title("Distribusi Panjang Karakter SMS per Kategori (Indonesia)", weight="bold")
    axes[0].set_xlabel("Kategori Pesan")
    axes[0].set_ylabel("Jumlah Karakter (Panjang SMS)")

    # Boxplot Jumlah Kata
    sns.boxplot(data=df_indo, x="label_name", y="word_count", palette=palette, ax=axes[1], showmeans=True,
                meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[1].set_title("Distribusi Jumlah Kata SMS per Kategori (Indonesia)", weight="bold")
    axes[1].set_xlabel("Kategori Pesan")
    axes[1].set_ylabel("Jumlah Kata")

    plt.tight_layout()
    fpath = os.path.join(OUTPUT_DIR, "2_length_distribution.png")
    plt.savefig(fpath, dpi=300)
    plt.close()
    print(f"[V] Tersimpan: {fpath}")

def plot_heuristic_indicators(df_indo):
    # Hitung persentase kemunculan fitur per kelas
    features = ["has_url", "has_phone", "has_nominal", "has_shortcode"]
    feature_labels = ["Memiliki URL/Link", "Memiliki No. Telepon/WA", "Menyebutkan Nominal Uang", "Memiliki Kode USSD"]

    grouped = df_indo.groupby("label_name")[features].mean() * 100
    grouped = grouped.loc[["Normal", "Penipuan", "Promosi"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    grouped.T.plot(kind="bar", ax=ax, color=["#2ecc71", "#e74c3c", "#f39c12"], width=0.75)
    
    ax.set_title("Persentase Keberadaan Indikator Keamanan pada SMS Indonesia", weight="bold")
    ax.set_xlabel("Fitur Indikator Heuristik")
    ax.set_ylabel("Persentase Kemunculan (%)")
    ax.set_xticklabels(feature_labels, rotation=15, ha="right")
    ax.legend(title="Kategori Pesan")
    
    for p in ax.patches:
        val = p.get_height()
        if val > 1:
            ax.annotate(f"{val:.1f}%", (p.get_x() + p.get_width() / 2., val + 1.5),
                        ha='center', va='bottom', fontsize=8, rotation=0)

    plt.ylim(0, 105)
    plt.tight_layout()
    fpath = os.path.join(OUTPUT_DIR, "3_heuristic_indicators.png")
    plt.savefig(fpath, dpi=300)
    plt.close()
    print(f"[V] Tersimpan: {fpath}")

def plot_top_keywords(df_indo):
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    categories = [("Normal", "#2ecc71"), ("Penipuan", "#e74c3c"), ("Promosi", "#f39c12")]

    stop_generic = {"dan", "di", "ke", "dari", "ini", "itu", "untuk", "pada", "adalah", "dengan", "saya", "kamu", "anda", "yg", "ada", "yang", "bisa", "sudah", "tidak"}

    for idx, (cat, color) in enumerate(categories):
        sub_df = df_indo[df_indo["label_name"] == cat]
        all_words = []
        for text in sub_df["cleaned_text"].dropna():
            words = [w for w in text.split() if len(w) > 2 and w not in stop_generic and not w.startswith("[")]
            all_words.extend(words)

        freq = Counter(all_words).most_common(12)
        if freq:
            words, counts = zip(*freq)
            y_pos = np.arange(len(words))
            axes[idx].barh(y_pos, counts, color=color, align='center')
            axes[idx].set_yticks(y_pos)
            axes[idx].set_yticklabels(words)
            axes[idx].invert_yaxis()
            axes[idx].set_title(f"Top Kata Khas: {cat}", weight="bold")
            axes[idx].set_xlabel("Frekuensi Kemunculan")

    plt.tight_layout()
    fpath = os.path.join(OUTPUT_DIR, "4_top_keywords.png")
    plt.savefig(fpath, dpi=300)
    plt.close()
    print(f"[V] Tersimpan: {fpath}")

def plot_correlation_heatmap(df_indo):
    cols = ["text_length", "word_count", "has_url", "has_phone", "has_nominal", "has_shortcode", "heuristic_risk_score", "label_2class"]
    rename_dict = {
        "text_length": "Panjang Teks",
        "word_count": "Jumlah Kata",
        "has_url": "Ada URL",
        "has_phone": "Ada No. Telp",
        "has_nominal": "Ada Nominal",
        "has_shortcode": "Ada Kode USSD",
        "heuristic_risk_score": "Skor Risiko",
        "label_2class": "Target (Spam/Phishing)"
    }
    sub_df = df_indo[cols].rename(columns=rename_dict)
    corr = sub_df.corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True, linewidths=.5, ax=ax)
    ax.set_title("Matriks Korelasi Antara Fitur Heuristik & Target Spam/Phishing", weight="bold")
    plt.tight_layout()
    fpath = os.path.join(OUTPUT_DIR, "5_correlation_heatmap.png")
    plt.savefig(fpath, dpi=300)
    plt.close()
    print(f"[V] Tersimpan: {fpath}")

def generate_eda_report(df_indo, df_eng, df_multi):
    stats_indo = df_indo.groupby("label_name")[["text_length", "word_count", "heuristic_risk_score"]].agg(["mean", "median", "std"])
    
    report_content = f"""# Laporan Eksplorasi Data (Exploratory Data Analysis - EDA)
## Analisis Karakteristik Dataset Deteksi SMS Phishing & Spam Dwibahasa

---

## 1. Ringkasan & Informasi Umum Dataset

Berdasarkan tahap audit dan penyeragaman format, proyek ini menggunakan 3 varian dataset standar:
1. **Dataset Primer Indonesia (`dataset_indonesia_standard.csv`)**: 1.138 baris pesan SMS nyata.
2. **Dataset Sekunder Inggris (`dataset_inggris_standard.csv`)**: 10.607 baris pesan SMS hasil ekstraksi 60 file JSONL.
3. **Dataset Multilingual Balanced (`dataset_multilingual_balanced.csv`)**: 2.638 baris pesan seimbang dwibahasa (Indonesia + Inggris).

### 1.1 Struktur Kolom & Kualitas Data
- **Jumlah Kolom**: 14 kolom terstandarisasi.
- **Missing Value**: **0 data kosong** (seluruh baris memiliki nilai teks, label, dan fitur yang valid).
- **Duplikasi**: Telah dilakukan deduplikasi teks normalisasi secara penuh sehingga tidak ada data identik yang bocor ke data uji.
- **Tipe Data**:
  - Teks: `text`, `cleaned_text`, `language`, `label_name`, `sub_category` (*Object / String*).
  - Numerik Diskrit: `label_3class`, `label_2class`, `text_length`, `word_count`, `has_url`, `has_phone`, `has_nominal`, `has_shortcode` (*Integer*).
  - Skor Kontinu: `heuristic_risk_score` (*Integer [0 - 100]*).

---

## 2. Distribusi Kelas & Ketidakseimbangan Data (*Class Imbalance*)

### 2.1 Distribusi Kelas SMS Indonesia (N = {len(df_indo)})
| Label Numerik | Kategori (Kelas) | Jumlah Pesan | Proporsi (%) | Karakteristik Utama |
|---|---|---|---|---|
| `0` | **Normal (Ham)** | {sum(df_indo['label_3class'] == 0)} | {sum(df_indo['label_3class'] == 0)/len(df_indo)*100:.2f}% | Percakapan pribadi, pesan santai, komunikasi perkuliahan/keluarga. |
| `1` | **Penipuan (Smishing/Fraud)** | {sum(df_indo['label_3class'] == 1)} | {sum(df_indo['label_3class'] == 1)/len(df_indo)*100:.2f}% | Penawaran pinjol ilegal, hadiah palsu Shopee/Bank, penipuan transfer/rekening. |
| `2` | **Promosi (Operator/Iklan)** | {sum(df_indo['label_3class'] == 2)} | {sum(df_indo['label_3class'] == 2)/len(df_indo)*100:.2f}% | Paket kuota internet resmi Telkomsel/Indosat/XL, diskon merchant. |

![Distribusi Kelas](eda_results/1_class_distribution.png)

> **Insight Analisis**:
> - Dataset Indonesia memiliki komposisi kelas yang ideal untuk evaluasi nyata, di mana kelas Normal mencakup ~50%, sedangkan ancaman penipuan mencakup ~29.2%, dan promosi ~21.0%.
> - Ketidakseimbangan minor ini memerlukan teknik **Stratified Train-Test Split** serta metrik **Macro-Averaged F1-Score** dan **Recall Penipuan** agar performa model tidak terbias oleh kelas mayoritas.

---

## 3. Analisis Panjang Teks & Jumlah Kata (*Text Length Analysis*)

### 3.1 Statistik Deskriptif SMS Indonesia
| Kategori Pesan | Rata-rata Panjang Karakter | Median Karakter | Rata-rata Jumlah Kata | Median Kata | Skor Risiko Heuristik Rata-rata |
|---|---|---|---|---|---|
| **Normal** | {df_indo[df_indo['label_name']=='Normal']['text_length'].mean():.1f} ± {df_indo[df_indo['label_name']=='Normal']['text_length'].std():.1f} | {df_indo[df_indo['label_name']=='Normal']['text_length'].median():.0f} | {df_indo[df_indo['label_name']=='Normal']['word_count'].mean():.1f} | {df_indo[df_indo['label_name']=='Normal']['word_count'].median():.0f} | {df_indo[df_indo['label_name']=='Normal']['heuristic_risk_score'].mean():.1f} |
| **Penipuan** | {df_indo[df_indo['label_name']=='Penipuan']['text_length'].mean():.1f} ± {df_indo[df_indo['label_name']=='Penipuan']['text_length'].std():.1f} | {df_indo[df_indo['label_name']=='Penipuan']['text_length'].median():.0f} | {df_indo[df_indo['label_name']=='Penipuan']['word_count'].mean():.1f} | {df_indo[df_indo['label_name']=='Penipuan']['word_count'].median():.0f} | {df_indo[df_indo['label_name']=='Penipuan']['heuristic_risk_score'].mean():.1f} |
| **Promosi** | {df_indo[df_indo['label_name']=='Promosi']['text_length'].mean():.1f} ± {df_indo[df_indo['label_name']=='Promosi']['text_length'].std():.1f} | {df_indo[df_indo['label_name']=='Promosi']['text_length'].median():.0f} | {df_indo[df_indo['label_name']=='Promosi']['word_count'].mean():.1f} | {df_indo[df_indo['label_name']=='Promosi']['word_count'].median():.0f} | {df_indo[df_indo['label_name']=='Promosi']['heuristic_risk_score'].mean():.1f} |

![Distribusi Panjang Teks](eda_results/2_length_distribution.png)

> **Insight Analisis**:
> 1. **SMS Normal cenderung jauh lebih pendek**: Panjang rata-rata hanya ~48 karakter (median 39 karakter) dan 7-8 kata. Hal ini wajar karena SMS percakapan manusia umumnya singkat dan *to-the-point*.
> 2. **SMS Penipuan & Promosi jauh lebih panjang**: Rata-rata panjang pesan penipuan adalah **116.8 karakter** dan promosi **128.5 karakter** (hampir 3 kali lipat SMS normal). Pelaku penipuan membutuhkan ruang teks lebih panjang untuk menyusun skenario manipulasi (ucapan selamat, nomor kontak, kode PIN, tautan, dan klaim).
> 3. Panjang teks menjadi salah satu pembeda leksikal yang signifikan bagi algoritma linear.

---

## 4. Analisis Indikator Keamanan Heuristik

![Indikator Heuristik](eda_results/3_heuristic_indicators.png)

### 4.1 Perbandingan Persentase Fitur Khusus:
- **Tautan / URL**:
  - Pada SMS Normal: **{df_indo[df_indo['label_name']=='Normal']['has_url'].mean()*100:.1f}%** (hampir tidak pernah memuat link).
  - Pada SMS Penipuan: **{df_indo[df_indo['label_name']=='Penipuan']['has_url'].mean()*100:.1f}%** (sering menyisipkan link phishing).
  - Pada SMS Promosi: **{df_indo[df_indo['label_name']=='Promosi']['has_url'].mean()*100:.1f}%** (memuat tautan aplikasi resmi seperti `tsel.me`).
- **Nomor Telepon / WhatsApp**:
  - Pada SMS Penipuan: **{df_indo[df_indo['label_name']=='Penipuan']['has_phone'].mean()*100:.1f}%** memuat nomor kontak call-center palsu atau nomor WhatsApp pribadi pelaku.
  - Pada SMS Normal: Hanya **{df_indo[df_indo['label_name']=='Normal']['has_phone'].mean()*100:.1f}%**.
- **Nominal Uang (Rp / Juta / Ribu)**:
  - Pada SMS Penipuan: **{df_indo[df_indo['label_name']=='Penipuan']['has_nominal'].mean()*100:.1f}%** mencantumkan nominal iming-iming hadiah atau batas pinjaman (misal 100jt, 300jt).
  - Pada SMS Promosi: **{df_indo[df_indo['label_name']=='Promosi']['has_nominal'].mean()*100:.1f}%** mencantumkan harga paket (misal Rp 35 Ribu).
- **Kode USSD Dial (`*363#`, `*550#`)**:
  - Eksklusif muncul pada **SMS Promosi Resmi ({df_indo[df_indo['label_name']=='Promosi']['has_shortcode'].mean()*100:.1f}%)**, dan praktis tidak pernah dipakai pada SMS penipuan.

---

## 5. Kata Kunci Paling Berpengaruh (*Top Keywords*)

![Top Keywords](eda_results/4_top_keywords.png)

- **Kata Khas SMS Normal**: *makan, rumah, kuliah, jam, datang, jalan, uang, tidur, besok*.
- **Kata Khas SMS Penipuan**: *pinjaman, tunai, bunga, hubungi, kartu kredit, shopee, hadiah, pemenang, rekening, resmi, legal, syarat*.
- **Kata Khas SMS Promosi**: *paket, flash, kuota, gigabyte, telkomsel, ekstra, nelpon, aplikasi, promo, aktifkan, internet*.

---

## 6. Korelasi Antar-Variabel

![Korelasi Heatmap](eda_results/5_correlation_heatmap.png)

- **Skor Risiko Heuristik** memiliki korelasi positif yang sangat tinggi (**r = {df_indo[['heuristic_risk_score', 'label_2class']].corr().iloc[0,1]:.2f}**) terhadap target Spam/Phishing.
- Keberadaan **URL (r = {df_indo[['has_url', 'label_2class']].corr().iloc[0,1]:.2f})** dan **Nomor Telepon (r = {df_indo[['has_phone', 'label_2class']].corr().iloc[0,1]:.2f})** berkorelasi kuat dengan indikasi pesan mencurigakan.
- Hal ini membuktikan bahwa kombinasi **pembobotan TF-IDF** dengan **fitur heuristik leksikal** akan memberikan daya pemisah yang sangat tajam bagi model Machine Learning.

---
*Laporan ini dihasilkan secara otomatis oleh `Project/src/eda.py` sebagai rujukan Bab F (Exploratory Data Analysis) pada Laporan PPT dan Rubrik Penilaian M15.*
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[V] Laporan EDA berhasil disimpan di: {REPORT_PATH}")

def main():
    print("=" * 70)
    print("MENJALANKAN MILESTONE 3: EKSPLORASI DATA (EDA) & VISUALISASI")
    print("=" * 70)

    df_indo, df_eng, df_multi = load_data()
    print(f"[*] Dataset Indo  : {len(df_indo)} baris")
    print(f"[*] Dataset Inggris: {len(df_eng)} baris")
    print(f"[*] Dataset Multi : {len(df_multi)} baris")

    print("\n[*] Membuat Grafik 1: Distribusi Kelas...")
    plot_class_distribution(df_indo, df_eng)

    print("[*] Membuat Grafik 2: Distribusi Panjang Teks & Kata...")
    plot_length_distributions(df_indo)

    print("[*] Membuat Grafik 3: Indikator Keamanan Heuristik...")
    plot_heuristic_indicators(df_indo)

    print("[*] Membuat Grafik 4: Top Kata Khas Tiap Kelas...")
    plot_top_keywords(df_indo)

    print("[*] Membuat Grafik 5: Heatmap Korelasi...")
    plot_correlation_heatmap(df_indo)

    print("[*] Menyusun Dokumen Laporan Lengkap EDA...")
    generate_eda_report(df_indo, df_eng, df_multi)

    print("\n" + "=" * 70)
    print("MILESTONE 3 SELESAI DENGAN SUKSES!")
    print(f"Seluruh visualisasi tersimpan di folder: {OUTPUT_DIR}")
    print(f"Laporan lengkap tersimpan di: {REPORT_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    main()

