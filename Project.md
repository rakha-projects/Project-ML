# Project Documentation & Activity Log
## Proyek Akhir Machine Learning: Deteksi SMS Phishing & Spam Berbahasa Indonesia Menggunakan Web Interaktif

---

## 1. Identitas & Gambaran Umum Proyek

- **Mata Kuliah:** Pembelajaran Mesin (Machine Learning) — Semester 5
- **Institusi:** Sekolah Vokasi — Teknologi Rekayasa Komputer
- **Fokus Folder Kerja:** `Project/` (Seluruh pengerjaan, aset, kode, model, dan dokumentasi dipusatkan di folder ini)
- **Topik / Tema:** Classification (Supervised Learning — Natural Language Processing / Text Classification)
- **Judul Proyek:** *Perbandingan Algoritma Machine Learning untuk Klasifikasi dan Deteksi SMS Phishing Berbahasa Indonesia Serta Implementasinya pada Web Interaktif*
- **Framework Web Terpilih (Kunci Memori):** **Streamlit** (`app.py` interaktif berbasis Python)
- **Platform Hosting Terpilih (Kunci Memori):** **Streamlit Community Cloud** (Terkoneksi langsung ke repositori GitHub, URL `*.streamlit.app`, 100% gratis, tanpa biaya server)
- **Teknologi Utama:** Python 3.12, Scikit-Learn, Streamlit, Pandas, NumPy, Matplotlib/Seaborn, Joblib
- **Rujukan Aturan & Rubrik:** Berdasarkan dokumen perkuliahan `deskripsi.md` (M15 - Project dan Refleksi) dan `Rencana_Proyek_ML_SMS_Indonesia.md`

> [!IMPORTANT]
> **KUNCI MEMORI SISTEM (LOCKED TECH-STACK)**:
> 1. Framework antarmuka web dikunci secara permanen menggunakan **Streamlit**.
> 2. Platform deployment dikunci menggunakan **Streamlit Community Cloud**.
> 3. Semua modul, pemanggilan model, dan interaksi pengguna harus dioptimasi secara spesifik untuk ekosistem Streamlit.

---

## 2. Status Proyek & Roadmap Pencapaian

```
[X] Milestone 1: Inisiasi Proyek & Penyusunan PRD & Project.md
[X] Milestone 2: Audit Dataset & Preprocessing Pipeline (Tahap 1 Selesai)
[X] Milestone 3: Eksplorasi Data (EDA) & Visualisasi (Selesai)
[X] Milestone 4: Training & Hyperparameter Tuning 3 Model (Selesai)
[X] Milestone 5: Evaluasi Komprehensif (Confusion Matrix, Macro-F1, Error Analysis) (Selesai)
[X] Milestone 6: Pembuatan Aplikasi Web Interaktif Berbasis Streamlit (Selesai)
[ ] Milestone 7: Penyusunan Laporan Akhir (Slide PPT) & Panduan Video Demo (<= 7 menit)
```

---

## 3. Struktur Direktori Proyek (`Project/`)

```text
Project/
│
├── Indonesia/                                  # Folder dataset lokal berbahasa Indonesia
│   ├── dataset_sms_spam_v1.csv                 # [Primer Asli] 1.143 SMS mentah (0=Normal, 1=Penipuan, 2=Promosi)
│   ├── dataset_clean.csv                       # [Hasil Audit] 1.138 SMS bersih terdeduplikasi
│   ├── dataset_indonesia_standard.csv          # [STANDAR TUNGGAL] 1.138 SMS Indo berskema 14 kolom seragam
│   ├── dataset_phishing_sms_indo.csv           # [Sekunder] 1.772 teks SMS & Email phishing biner + sub-kategori
│   └── indo_dataset.xlsx                       # Dataset IndoTRUE-Net (15.000 medsos - referensi cadangan)
│
├── Inggris/                                    # Folder dataset bahasa Inggris
│   ├── clean-*.jsonl (60 berkas)               # [Korpus Asli] 119.105 pesan teks mentah JSONL
│   └── dataset_inggris_standard.csv            # [STANDAR TUNGGAL] 10.607 SMS Inggris berskema 14 kolom seragam
│
├── dataset_multilingual_balanced.csv           # [STANDAR GABUNGAN] 2.638 SMS seimbang dwibahasa (ID + EN)
│
├── eda_results/                                # [Visualisasi EDA] Grafik statistik resolusi tinggi (300 DPI)
│   ├── 1_class_distribution.png               # Grafik perbandingan distribusi kelas (ID & EN)
│   ├── 2_length_distribution.png              # Boxplot perbandingan panjang karakter & kata per kelas
│   ├── 3_heuristic_indicators.png              # Persentase kemunculan URL, telepon, uang, USSD per kelas
│   ├── 4_top_keywords.png                      # Top 12 kata kunci khas untuk Normal, Penipuan, Promosi
│   ├── 5_correlation_heatmap.png               # Heatmap korelasi Pearson antara fitur & target
│   ├── confusion_matrices.png                  # Heatmap matriks kebingungan 3 model pembanding
│   └── feature_importance.png                  # Grafik bobot fitur/kata pemicu keputusan model
│
├── EDA_Report.md                               # [Laporan Komprehensif EDA] Analisis statistik & insight
├── Evaluation_Report.md                        # [Laporan Evaluasi & Error Analysis] Bedah performa model
├── deskripsi.md                                # Panduan resmi & rubrik penilaian M15 dari dosen
├── Rencana_Proyek_ML_SMS_Indonesia.md          # Dokumen rencana awal dan rujukan literatur proyek
├── SMS_DATASET_FOR_MULTI-CLASS_...pdf          # Referensi paper ilmiah dataset SMS
│
├── PRD.md                                      # Product Requirements Document (Spesifikasi Fitur Lengkap)
├── Project.md                                  # Dokumentasi Proyek & Riwayat Perubahan (Selalu di-update)
├── requirements.txt                            # Daftar pustaka dependensi Python (pandas, sklearn, streamlit, dll)
│
├── src/                                        # Modul source code pipeline ML
│   ├── __init__.py
│   ├── preprocessing.py                        # Preprocessing bilingual, entity masking, & deteksi bahasa
│   ├── audit_dataset.py                        # Audit missing value & deduplikasi dataset primer
│   ├── unify_datasets.py                       # Penyeragaman skema data Indonesia & Inggris ke format identik
│   ├── eda.py                                  # Skrip analisis statistik deskriptif & pembangkit visualisasi
│   ├── train.py                                # Skrip pelatihan model, cross-validation, dan ekspor .joblib
│   └── evaluate.py                             # Skrip evaluasi komprehensif, overfitting check & error analysis
│
├── models/                                     # File penyimpanan model terlatih (.joblib) & hasil evaluasi
│   ├── tfidf_vectorizer_id.joblib              # Ekstraktor TF-IDF bahasa Indonesia (3.006 fitur n-gram)
│   ├── multinomial_naive_bayes_id.joblib       # Model 1: Multinomial NB Indonesia (Acc: 96.05%, F1: 95.27%)
│   ├── logistic_regression_id.joblib          # Model 2: Logistic Regression Indonesia (Acc: 97.37%, F1: 96.68%)
│   ├── linear_svm_id.joblib                    # Model 3: Linear SVM Terkalibrasi (Acc: 97.37%, F1: 96.68%)
│   ├── best_model_id.joblib                    # Pointer model terbaik terpilih (Logistic Regression)
│   ├── tfidf_vectorizer_en.joblib              # Ekstraktor TF-IDF bahasa Inggris
│   ├── best_model_en.joblib                    # Model terbaik bahasa Inggris (Acc: 91.00%, F1: 89.81%)
│   ├── model_comparison_id.csv                 # Tabel perbandingan metrik evaluasi (CSV)
│   └── model_comparison_id.json                # Tabel perbandingan metrik evaluasi (JSON)
│
├── app.py                                      # Aplikasi antarmuka Web Interaktif Streamlit (Desain example.html)
├── example.html                                # Berkas referensi desain UI/UX (Navy/Slate palette & Typography)
└── laporan/                                    # [Rencana] PPT Laporan & Naskah Video Demo
```

---

## 4. Inventaris & Audit Karakteristik Dataset

| Nama Berkas | Jumlah Baris | Bahasa | Format & Skema | Kelas / Target | Peran dalam Proyek |
|---|---|---|---|---|---|
| `dataset_indonesia_standard.csv` | 1.138 SMS | Indonesia | **Standar Tunggal (14 Kolom Identik)** | • 0: Normal (49.8%)<br>• 1: Penipuan (29.2%)<br>• 2: Promosi (21.0%) | **Dataset Utama Indonesia**. Hasil audit, pembersihan, dan deduplikasi lengkap. |
| `dataset_inggris_standard.csv` | 10.607 SMS | Inggris | **Standar Tunggal (14 Kolom Identik)** | • 0: Normal (28.3%)<br>• 1: Penipuan/Scam (52.2%)<br>• 2: Promosi (19.5%) | **Dataset Utama Inggris**. Diekstrak dari 60 file JSONL dengan skema kolom yang persis sama. |
| `dataset_multilingual_balanced.csv` | 2.638 SMS | Dwibahasa (ID+EN) | **Standar Tunggal (14 Kolom Identik)** | 3 Kelas Seimbang (Normal, Penipuan, Promosi) | **Dataset Multilingual**. Gabungan sampel seimbang ID + EN untuk pelatihan model lintas bahasa. |
| `dataset_sms_spam_v1.csv` | 1.143 SMS | Indonesia | CSV Mentah (Teks, label) | 3 Kelas (Yudi Wibisono) | Sumber data mentah lokal Indonesia. |
| `clean-*.jsonl` (60 berkas) | 119.105 baris | Inggris | JSONL Mentah | Multi-kategori Inggris | Sumber data mentah internasional. |

> **Skema 14 Kolom Seragam (Universal Schema)**:
> `text`, `cleaned_text`, `language`, `label_3class`, `label_2class`, `label_name`, `sub_category`, `text_length`, `word_count`, `has_url`, `has_phone`, `has_nominal`, `has_shortcode`, `heuristic_risk_score`.

---

## 5. Rencana Pembagian Tugas Kelompok (Sesuai Ketentuan M15)

Sesuai ketentuan perkuliahan, kelompok beranggotakan 3 orang mahasiswa dengan pembagian tugas:

| Peran Anggota | Tanggung Jawab Utama | Rincian Luaran |
|---|---|---|
| **Mahasiswa 1** | *Data Engineer & EDA Specialist* | Audit dataset, pembersihan data (*data cleaning*), penanganan duplikasi, normalisasi singkatan bahasa Indonesia, visualisasi EDA, penyusunan dokumentasi karakteristik data. |
| **Mahasiswa 2** | *Machine Learning Engineer* | Pembangunan pipeline ekstraksi fitur (TF-IDF), pelatihan 3 algoritma (Multinomial NB, Logistic Regression, Linear SVM), validasi silang (Stratified K-Fold), evaluasi metrik, analisis kesalahan (*error analysis*). |
| **Mahasiswa 3** | *Web Application & Deployment Lead* | Pengembangan antarmuka web Streamlit (Input, Single Scanner, Preset Examples, Batch CSV, Dashboard Evaluasi), pengujian end-to-end, penyusunan slide PPT laporan dan skenario video demo. |

> *Catatan: Seluruh anggota kelompok wajib memahami keseluruhan alur sistem untuk kesiapan sesi tanya jawab individu saat ujian.*

---

## 6. Riwayat Perubahan (Changelog & Activity Tracking)

> **Komitmen Pembaruan:** Dokumen ini akan diperbarui pada setiap iterasi/perintah prompt untuk merekam semua tindakan, perkembangan implementasi, dan keputusan teknis yang telah diambil.

### [2026-10-30 - Sesi 10] - Eksekusi Milestone 6: Pembangunan Aplikasi Web Streamlit Mengadopsi Desain example.html
- **Pengembangan Antarmuka Interaktif (`Project/app.py`)**:
  - Mengadopsi secara akurat sistem desain (*design tokens*) dari [**`Project/example.html`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/example.html):
    - *Tipografi*: Google Fonts `Plus Jakarta Sans` dan `Poppins` (tebal, modern, dan elegan).
    - *Palet Warna*: Navy Primer (`#263142`), Background Luar Slate (`#cbd5dc`), Paper-Sheet Card Putih (`#ffffff`) dengan *floating soft shadow*, aksen Emerald (`#2ecc71`), Coral Red (`#e74c3c`), dan Amber Gold (`#f39c12`).
    - *Struktur Layout*: Navbar geometric brand `SMISHINGGUARD`, Hero card dengan gradien navy atmosferik, 4 stat-badge pills, dan rounded input pills.
- **Implementasi 4 Tab Fungsional Lengkap**:
  1. *Tab 1 (Pemindai SMS Real-Time)*: Mendukung deteksi otomatis bahasa (Indonesia / Inggris), 4 tombol preset contoh pesan instan, meter probabilitas 3-kelas, lencana risiko heuristik (URL, telepon pribadi, uang, USSD), dan rekomendasi tindakan keamanan.
  2. *Tab 2 (Pemeriksaan Massal via CSV)*: Fitur unggah file CSV, pemindaian kolektif otomatis, ringkasan metrik batch, dan tombol ekspor hasil unduhan (`Hasil_Deteksi_SMS_Batch.csv`).
  3. *Tab 3 (Dashboard Evaluasi & Transparansi Akademik)*: Menampilkan tabel perbandingan 3 model Scikit-Learn, visualisasi Confusion Matrix heatmap, grafik Feature Importance, dan analisis overfitting/underfitting untuk bahan presentasi dosen.
  4. *Tab 4 (Panduan Anatomi Modus Smishing)*: Kartu edukasi interaktif 4 modus kejahatan SMS paling umum di Indonesia (Modus APK Kurir, Undian Shopee, Pinjol Ilegal, dan Rekening Diblokir).
- **Pengujian Kompilasi Script**:
  - Script `app.py` berhasil diuji dan dikompilasi bebas dari syntax error.
- **Status Proyek**:
  - Menandai **Milestone 6 (Pembuatan Aplikasi Web Interaktif Berbasis Streamlit)** sebagai SELESAI.

### [2026-10-30 - Sesi 9] - Panduan Monitoring Background Task & Status Eksekusi
- **Penjelasan Mekanisme Monitoring Task**:
  - Menjelaskan kepada pengguna 4 cara untuk memantau proses komputasi yang berjalan di latar belakang (*background tasks*):
    1. Melalui kartu eksekusi perintah di antarmuka chat UI (*Expand Terminal Output*).
    2. Membaca file log langsung di direktori `.system_generated/tasks/task-<id>.log`.
    3. Memeriksa status secara interaktif via perintah chat (*agentic task polling*).
    4. Sistem notifikasi otomatis (*Reactive Wakeup*) saat komputasi selesai.
  - Melakukan pembersihan (*cleanup*) terhadap seluruh handle proses latar belakang yang telah selesai.

### [2026-10-30 - Sesi 8] - Eksekusi Milestone 5: Evaluasi Komprehensif, Overfitting Check & Error Analysis
- **Pemeriksaan Overfitting vs Underfitting (`Project/src/evaluate.py`)**:
  - Menguji performa data latih vs data uji:
    - Logistic Regression: Train Acc = 99.45% vs Test Acc = 97.37% (Gap: +2.08%).
    - Train Macro-F1 = 99.38% vs Test Macro-F1 = 96.68% (Gap: +2.70%).
    - Terbukti secara empiris berstatus **Optimal / Good Fit** (tidak menghafal data dan memiliki generalisasi tinggi).
- **Analisis Mendalam Kesalahan Prediksi (*Error Analysis*)**:
  - Mengidentifikasi 6 sampel SMS yang salah diprediksi dari 228 data uji (Error rate 2.63%).
  - Membedah akar masalah:
    - Modus penipuan berkedok percakapan santai (*social engineering*) seperti modus "Bella bingung bang...".
    - Modus penipuan kuota gratis yang meniru buletin promo resmi operator.
    - Notifikasi resmi bank yang terpicu oleh kata sensitif seperti "PIN rahasia" dan "rekening".
  - Mencapai **Recall 100% pada SMS Normal** (tidak ada pesan normal yang terblokir atau memicu alarm palsu).
- **Ekstraksi Feature Importance / Kata Kunci Penentu**:
  - Menghasilkan grafik [**`Project/eda_results/feature_importance.png`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/eda_results/feature_importance.png) yang menampilkan 12 fitur paling berpengaruh pada masing-masing kelas:
    - Penipuan dipicu oleh: token `[nomor]`, `pinjaman`, `tunai`, `bunga`, `shopee`, `rekening`.
    - Promosi dipicu oleh: `kuota`, `gigabyte`, `paket`, `flash`, `[kode]`, `berlaku`.
    - Normal dipicu oleh leksikon percakapan santai: `makan`, `rumah`, `kuliah`, `datang`, `tidur`.
- **Penyusunan Laporan Evaluasi (`Project/Evaluation_Report.md`)**:
  - Menyusun laporan komprehensif yang menjawab seluruh 7 poin ketentuan Bab 10 (Analisis Model) dan Bab N (Keterbatasan & Pengembangan) pada rubrik M15.
- **Status Proyek**:
  - Menandai **Milestone 5 (Evaluasi Komprehensif & Analisis Model)** sebagai SELESAI.

### [2026-10-30 - Sesi 7] - Eksekusi Milestone 4: Pelatihan & Perbandingan 3 Model Machine Learning
- **Pembuatan Pipeline Pelatihan (`Project/src/train.py`)**:
  - Melakukan *Stratified 80:20 Train-Test Split* (910 train : 228 test) untuk menjamin data uji murni independen tanpa *data leakage*.
  - Ekstraksi fitur menggunakan `TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)` menghasilkan **3.006 fitur n-gram leksikal**.
  - Melatih dan membandingkan **3 algoritma machine learning** dengan validasi silang (5-Fold Stratified CV):
    1. **Multinomial Naive Bayes** (`alpha=0.3`):
       - Accuracy: **96.05%** | Macro F1-Score: **95.27%** | Recall Penipuan: **89.39%**
       - 5-Fold CV Macro-F1: 0.9374 ± 0.0165
    2. **Logistic Regression** (`C=2.5, class_weight='balanced'`):
       - Accuracy: **97.37%** | Macro F1-Score: **96.68%** | Recall Penipuan: **95.45%** | Recall Normal: **100%**
       - 5-Fold CV Macro-F1: 0.9410 ± 0.0155 (Tertinggi)
    3. **Linear SVM (Terkalibrasi CalibratedClassifierCV)** (`C=1.0, class_weight='balanced'`):
       - Accuracy: **97.37%** | Macro F1-Score: **96.68%** | Recall Penipuan: **95.45%**
       - 5-Fold CV Macro-F1: 0.9360 ± 0.0116
- **Pemilihan Model Terbaik (Justifikasi Ilmiah)**:
  - **Logistic Regression** dipilih sebagai model utama karena memiliki **5-Fold CV Macro-F1 tertinggi (0.9410)**, **Recall Penipuan sangat tinggi (95.45%)** sehingga minim meloloskan SMS penipuan berbahaya, serta secara alami menghasilkan estimasi probabilitas terkalibrasi (`predict_proba()`) untuk meter keyakinan di web Streamlit.
- **Model Bahasa Inggris (Multilingual Support)**:
  - Melatih model Logistic Regression untuk korpus Inggris (10.607 baris) menghasilkan **Akurasi 91.00%** dan **Macro F1-Score 89.81%**.
- **Penyimpanan Artefak & Visualisasi**:
  - Seluruh model terlatih, vectorizer, dan tabel metrik perbandingan tersimpan rapi di folder [**`Project/models/`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/models).
  - Visualisasi Confusion Matrix ketiga algoritma tersimpan di [**`Project/eda_results/confusion_matrices.png`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/eda_results/confusion_matrices.png).
- **Status Proyek**:
  - Menandai **Milestone 4 (Training & Hyperparameter Tuning 3 Model)** sebagai SELESAI.

### [2026-10-30 - Sesi 6] - Eksekusi Milestone 3: Eksplorasi Data (EDA) & Visualisasi Lengkap
- **Pembuatan Modul Analisis & Visualisasi (`Project/src/eda.py`)**:
  - Mengembangkan skrip otomatis untuk menghasilkan ringkasan statistik deskriptif, uji korelasi, dan 5 grafik analisis data berkualitas tinggi (300 DPI) di folder `Project/eda_results/`:
    1. `1_class_distribution.png`: Visualisasi distribusi kelas SMS Indonesia (N=1.138) dan Inggris (N=10.607).
    2. `2_length_distribution.png`: Boxplot panjang karakter dan jumlah kata per kelas (menemukan bahwa SMS penipuan rata-rata 150.6 karakter, jauh lebih panjang dari SMS normal 70.5 karakter).
    3. `3_heuristic_indicators.png`: Grafik persentase fitur URL, kontak telepon, nominal uang, dan kode USSD per kategori.
    4. `4_top_keywords.png`: Grafik batang frekuensi kata kunci paling khas (*distinctive words*) untuk Normal, Penipuan, dan Promosi.
    5. `5_correlation_heatmap.png`: Heatmap korelasi matriks Pearson antara fitur heuristik dan target label.
- **Penyusunan Laporan EDA (`Project/EDA_Report.md`)**:
  - Menyusun dokumen laporan komprehensif berisi penjelasan statistik, perbandingan karakteristik kelas, dan insight ilmiah yang siap disalin langsung ke slide PPT (Bab F) sesuai rubrik penilaian M15.
- **Pembaruan Status Proyek**:
  - Menandai **Milestone 3 (Eksplorasi Data & Visualisasi)** sebagai SELESAI.

### [2026-10-30 - Sesi 5] - Standardisasi Format Dataset Dwibahasa & Mesin Deteksi Bahasa Otomatis
- **Penyeragaman Format Data (Universal Schema Standardization)**:
  - Mengonversi dataset Indonesia dan dataset Inggris (60 file JSONL) ke dalam struktur format CSV standar yang **100% identik** dengan 14 kolom seragam.
  - Menghasilkan 3 berkas dataset standar siap olah:
    1. [**`Project/Indonesia/dataset_indonesia_standard.csv`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/Indonesia/dataset_indonesia_standard.csv) (1.138 baris).
    2. [**`Project/Inggris/dataset_inggris_standard.csv`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/Inggris/dataset_inggris_standard.csv) (10.607 baris terstandarisasi).
    3. [**`Project/dataset_multilingual_balanced.csv`**](file:///c:/Users/user/Documents/Semester%205/Machine%20Learning/Project/dataset_multilingual_balanced.csv) (2.638 baris dwibahasa seimbang).
- **Pengembangan Mesin Deteksi Bahasa Otomatis (`Project/src/preprocessing.py`)**:
  - Membangun fungsi `detect_language(text)` untuk memilah secara akurat apakah SMS berbahasa Indonesia atau Inggris.
  - Menambahkan kamus slang & kontraksi bahasa Inggris (`EN_SLANG_DICTIONARY`) seperti `u` $\rightarrow$ `you`, `txt` $\rightarrow$ `text`, `pls` $\rightarrow$ `please`.
  - Memperluas regex entitas untuk mengenali mata uang internasional (`$`, `£`, `€`) dan nomor telepon Inggris/internasional.
  - Memperbarui `clean_text(text, lang='auto')` dan `extract_heuristic_features(text, lang='auto')` untuk pemrosesan dwibahasa.
- **Pembaruan PRD (`Project/PRD.md`)**:
  - Menambahkan spesifikasi fitur *Auto-Detect Language* pada antarmuka web Streamlit.

### [2026-10-30 - Sesi 4] - Penguncian Memori Permanen: Streamlit & Streamlit Community Cloud
- **Penguncian Memori Sistem (Locked Memory)**:
  - User secara eksplisit menginstruksikan bahwa antarmuka web dan arsitektur deployment dikunci permanen menggunakan **Streamlit** dan **Streamlit Community Cloud**.
  - Bagian *Identitas Proyek* (Bab 1) telah ditambahkan blok peringatan penting (*Alert Callout*) agar seluruh sesi pengembangan masa depan konsisten mengacu pada standar Streamlit.
  - Memastikan seluruh modul visualisasi, inferensi real-time, dan batch prediction dirancang spesifik untuk `st.set_page_config`, `st.sidebar`, `st.metric`, dan komponen Streamlit lainnya.

### [2026-10-30 - Sesi 3] - Konsultasi & Pemilihan Platform Hosting Web
- **Evaluasi Opsi Deployment Aplikasi Web Streamlit**:
  - Merinci dan membandingkan 4 platform hosting yang relevan untuk proyek akademik ML:
    1. **Streamlit Community Cloud** (Opsi Utama & Sangat Direkomendasikan): Gratis, langsung terhubung ke repositori GitHub, auto-deploy saat git push, domain resmi `*.streamlit.app`.
    2. **Hugging Face Spaces** (Opsi ML Populer): Gratis, ekosistem AI terstandar, mendukung SDK Streamlit secara *out-of-the-box*.
    3. **Render (render.com)**: Layanan PaaS fleksibel untuk deployment aplikasi berbasis Python/Web Service.
    4. **Cloudflare Tunnel / ngrok**: Solusi port-forwarding untuk demonstrasi langsung (*live demo*) saat presentasi di kelas tanpa perlu deploy publik.
  - Memastikan dependensi di `requirements.txt` dan skrip `app.py` dirancang kompatibel untuk langsung *deploy* ke Streamlit Community Cloud.

### [2026-10-30 - Sesi 2] - Eksekusi Tahap 1: Instalasi Dependensi, Preprocessing Pipeline & Audit Dataset
- **Instalasi Ekosistem Machine Learning**:
  - Menginstal pustaka Python: `pandas` (3.1.0), `scikit-learn` (1.9.1), `numpy` (2.5.4), `joblib` (1.6.0), `streamlit` (1.66.1), `matplotlib` (3.11.2), dan `seaborn` (0.13.2).
  - Menyusun file dependensi proyek di `Project/requirements.txt`.
- **Pengembangan Modul Preprocessing (`Project/src/preprocessing.py`)**:
  - Mengimplementasikan kamus normalisasi kata slang/singkatan SMS Indonesia (*kamus alay*) dengan lebih dari 100 lema kosakata populer (`dpt` $\rightarrow$ `dapat`, `sy` $\rightarrow$ `saya`, `hub` $\rightarrow$ `hubungi`, `rek` $\rightarrow$ `rekening`, `tsel` $\rightarrow$ `telkomsel`, dll).
  - Mengimplementasikan *entity masking* berbasis regular expression:
    - Tautan web/link shortener $\rightarrow$ `[url]`
    - Nomor telepon / kontak WA $\rightarrow$ `[nomor]`
    - Nominal uang / rupiah $\rightarrow$ `[nominal]`
    - Kode USSD operator $\rightarrow$ `[kode]`
  - Menghapus timestamp otomatis operator dan karakter noise non-alphanumeric.
  - Membangun fungsi `extract_heuristic_features()` untuk mendeteksi indikator risiko (URL, nomor, nominal, kode, kata urgensi, kata finansial, serta estimasi skor risiko 0-100).
- **Audit & Deduplikasi Dataset (`Project/src/audit_dataset.py`)**:
  - Membaca dataset primer `Project/Indonesia/dataset_sms_spam_v1.csv` (1.143 baris).
  - Hasil audit missing value: 0 baris kosong/invalid.
  - Menangani deduplikasi teks normalisasi: Menghasilkan 1.138 sampel bersih bebas redudansi lintas data latih dan uji.
  - Menghasilkan file dataset bersih siap latih: `Project/Indonesia/dataset_clean.csv`.
  - Distribusi data bersih:
    - **Kelas 0 (Normal)**: 567 sampel (49.82%)
    - **Kelas 1 (Penipuan)**: 332 sampel (29.17%)
    - **Kelas 2 (Promosi)**: 239 sampel (21.00%)

### [2026-10-30 - Sesi 1] - Inisiasi Proyek & Penetapan Fondasi Produk
- **Identifikasi Permintaan & Ruang Lingkup**:
  - Menetapkan fokus kerja 100% berada pada folder `Project/`.
  - Menganalisis dokumen acuan `deskripsi.md` (syarat kelulusan M15), `Rencana_Proyek_ML_SMS_Indonesia.md`, serta materi kuliah Semester 5.
- **Audit Dataset Lokal**:
  - Menginspeksi folder `Project/Indonesia/` dan `Project/Inggris/`.
  - Memverifikasi skema data `dataset_sms_spam_v1.csv` (1.143 baris, 3 kelas: Normal, Penipuan, Promosi) sebagai dataset primer.
  - Memverifikasi `dataset_phishing_sms_indo.csv` (1.772 baris) sebagai korpus validasi pengayaan pola phishing.
- **Penyusunan Berkas Utama**:
  - Membuat `Project/PRD.md` (Product Requirements Document) yang merinci seluruh arsitektur sistem, 4 modul web interaktif, kriteria non-fungsional, dan acceptance criteria.
  - Membuat `Project/Project.md` sebagai berkas pusat pelacakan status proyek dan log perubahan otomatis.
- **Strategi Modeling Ditetapkan**:
  - Menentukan 3 algoritma wajib: Multinomial Naive Bayes, Logistic Regression, dan Linear Support Vector Machine.
  - Menentukan metrik evaluasi prioritas: Recall pada kelas Penipuan (mencegah *false negative* ancaman) dan Macro-Averaged F1-Score.

---

## 7. Rencana Aksi Berikutnya (Next Action Items)
1. **Milestone 6 (Pengembangan Web Streamlit `app.py`)**:
   - Membangun antarmuka interaktif di `Project/app.py` sesuai spesifikasi di `PRD.md`.
   - Mengintegrasikan modul `preprocessing.py` dwibahasa, deteksi bahasa otomatis, dan pemanggilan artefak model `Project/models/best_model_id.joblib` serta `best_model_en.joblib`.
   - Mengimplementasikan 4 modul antarmuka: Single SMS Scanner, Preset Contoh Pesan, Analisis Heuristik & Explainable AI, Batch CSV Upload, serta Dashboard Evaluasi Model.
2. **Milestone 7 (Laporan PPT & Naskah Video Demo)**:
   - Menyusun slide presentasi PPT sesuai struktur M15 (Bab A s.d. O).
   - Menyiapkan naskah dan panduan perekaman video live execution aplikasi durasi <= 7 menit.

