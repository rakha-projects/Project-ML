# Laporan Eksplorasi Data (Exploratory Data Analysis - EDA)
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

### 2.1 Distribusi Kelas SMS Indonesia (N = 1138)
| Label Numerik | Kategori (Kelas) | Jumlah Pesan | Proporsi (%) | Karakteristik Utama |
|---|---|---|---|---|
| `0` | **Normal (Ham)** | 567 | 49.82% | Percakapan pribadi, pesan santai, komunikasi perkuliahan/keluarga. |
| `1` | **Penipuan (Smishing/Fraud)** | 332 | 29.17% | Penawaran pinjol ilegal, hadiah palsu Shopee/Bank, penipuan transfer/rekening. |
| `2` | **Promosi (Operator/Iklan)** | 239 | 21.00% | Paket kuota internet resmi Telkomsel/Indosat/XL, diskon merchant. |

![Distribusi Kelas](eda_results/1_class_distribution.png)

> **Insight Analisis**:
> - Dataset Indonesia memiliki komposisi kelas yang ideal untuk evaluasi nyata, di mana kelas Normal mencakup ~50%, sedangkan ancaman penipuan mencakup ~29.2%, dan promosi ~21.0%.
> - Ketidakseimbangan minor ini memerlukan teknik **Stratified Train-Test Split** serta metrik **Macro-Averaged F1-Score** dan **Recall Penipuan** agar performa model tidak terbias oleh kelas mayoritas.

---

## 3. Analisis Panjang Teks & Jumlah Kata (*Text Length Analysis*)

### 3.1 Statistik Deskriptif SMS Indonesia
| Kategori Pesan | Rata-rata Panjang Karakter | Median Karakter | Rata-rata Jumlah Kata | Median Kata | Skor Risiko Heuristik Rata-rata |
|---|---|---|---|---|---|
| **Normal** | 70.5 ± 46.3 | 59 | 12.1 | 11 | 1.8 |
| **Penipuan** | 150.6 ± 49.5 | 150 | 21.0 | 19 | 49.6 |
| **Promosi** | 140.6 ± 34.8 | 142 | 21.5 | 21 | 18.4 |

![Distribusi Panjang Teks](eda_results/2_length_distribution.png)

> **Insight Analisis**:
> 1. **SMS Normal cenderung jauh lebih pendek**: Panjang rata-rata hanya **70.5 karakter** (median 59 karakter) dan 11-12 kata. Hal ini wajar karena SMS percakapan manusia umumnya singkat dan *to-the-point*.
> 2. **SMS Penipuan & Promosi jauh lebih panjang**: Rata-rata panjang pesan penipuan mencapai **150.6 karakter** dan promosi **140.6 karakter** (lebih dari 2 kali lipat SMS normal). Pelaku penipuan membutuhkan ruang teks lebih panjang untuk menyusun skenario manipulasi (ucapan selamat, nomor kontak, kode PIN, tautan, dan klaim).
> 3. Panjang teks menjadi salah satu pembeda leksikal yang signifikan bagi algoritma linear.

---

## 4. Analisis Indikator Keamanan Heuristik

![Indikator Heuristik](eda_results/3_heuristic_indicators.png)

### 4.1 Perbandingan Persentase Fitur Khusus:
- **Tautan / URL**:
  - Pada SMS Normal: **0.5%** (hampir tidak pernah memuat link).
  - Pada SMS Penipuan: **52.1%** (sering menyisipkan link phishing).
  - Pada SMS Promosi: **29.3%** (memuat tautan aplikasi resmi seperti `tsel.me`).
- **Nomor Telepon / WhatsApp**:
  - Pada SMS Penipuan: **40.1%** memuat nomor kontak call-center palsu atau nomor WhatsApp pribadi pelaku.
  - Pada SMS Normal: Hanya **0.0%**.
- **Nominal Uang (Rp / Juta / Ribu)**:
  - Pada SMS Penipuan: **37.0%** mencantumkan nominal iming-iming hadiah atau batas pinjaman (misal 100jt, 300jt).
  - Pada SMS Promosi: **43.9%** mencantumkan harga paket (misal Rp 35 Ribu).
- **Kode USSD Dial (`*363#`, `*550#`)**:
  - Eksklusif muncul pada **SMS Promosi Resmi (41.8%)**, dan praktis tidak pernah dipakai pada SMS penipuan.

---

## 5. Kata Kunci Paling Berpengaruh (*Top Keywords*)

![Top Keywords](eda_results/4_top_keywords.png)

- **Kata Khas SMS Normal**: *makan, rumah, kuliah, jam, datang, jalan, uang, tidur, besok*.
- **Kata Khas SMS Penipuan**: *pinjaman, tunai, bunga, hubungi, kartu kredit, shopee, hadiah, pemenang, rekening, resmi, legal, syarat*.
- **Kata Khas SMS Promosi**: *paket, flash, kuota, gigabyte, telkomsel, ekstra, nelpon, aplikasi, promo, aktifkan, internet*.

---

## 6. Korelasi Antar-Variabel

![Korelasi Heatmap](eda_results/5_correlation_heatmap.png)

- **Skor Risiko Heuristik** memiliki korelasi positif yang sangat tinggi (**r = 0.65**) terhadap target Spam/Phishing.
- Keberadaan **URL (r = 0.51)** dan **Nomor Telepon (r = 0.37)** berkorelasi kuat dengan indikasi pesan mencurigakan.
- Hal ini membuktikan bahwa kombinasi **pembobotan TF-IDF** dengan **fitur heuristik leksikal** akan memberikan daya pemisah yang sangat tajam bagi model Machine Learning.

---
*Laporan ini dihasilkan secara otomatis oleh `Project/src/eda.py` sebagai rujukan Bab F (Exploratory Data Analysis) pada Laporan PPT dan Rubrik Penilaian M15.*
