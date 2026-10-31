# Product Requirements Document (PRD)
## Web Aplikasi Deteksi SMS Phishing & Spam Berbahasa Indonesia (Smishing Detector)

---

## 1. Ringkasan Eksekutif (Executive Summary)

### 1.1 Latar Belakang Masalah
Kejahatan siber berbasis rekayasa sosial (*social engineering*) melalui pesan singkat (SMS), atau yang dikenal sebagai **SMS Phishing (Smishing)** dan penipuan SMS (*fraud*), kian marak terjadi di Indonesia. Modus yang umum digunakan meliputi:
- Undian berhadiah palsu (pemberian uang tunai, hadiah mobil/motor).
- Tawaran pinjaman online (pinjol) ilegal tanpa agunan.
- Pencurian kredensial perbankan/finansial dan permintaan kode OTP.
- Distribusi tautan berbahaya (*malicious link*) serta file APK berbahaya (kedok kurir paket, undangan pernikahan, surat tilang).
- Notifikasi darurat palsu (keluarga kecelakaan, pemblokiran rekening).

Masyarakat kerap kesulitan membedakan antara pesan normal (komunikasi pribadi/kedinasan), pesan promosi resmi dari operator telekomunikasi atau merchant, dan pesan phishing/penipuan yang berbahaya.

### 1.2 Tujuan Produk
Membangun aplikasi web berbasis Machine Learning yang mampu:
1. Menerima masukan teks SMS berbahasa Indonesia dari pengguna.
2. Memproses dan menganalisis teks secara otomatis (*preprocessing* dan ekstraksi fitur TF-IDF).
3. Mengklasifikasikan SMS ke dalam kategori yang tepat: **Normal**, **Promosi**, atau **Penipuan/Phishing** (serta opsi biner: **Phishing** vs **Normal**).
4. Menyajikan probabilitas keyakinan model (*confidence score*), visualisasi indikator ancaman (deteksi tautan, nomor kontak, kata pemicu), serta rekomendasi tindakan preventif secara transparan (*explainable*).
5. Memenuhi seluruh kriteria akademik Tugas Akhir Mata Kuliah Pembelajaran Mesin (M15), termasuk perbandingan $\ge 3$ algoritma, evaluasi komprehensif, dan siap didemokan secara interaktif.

---

## 2. Sasaran Pengguna & Skenario Penggunaan (User Personas & Use Cases)

### 2.1 Target Pengguna
- **Masyarakat Umum / Pengguna Ponsel**: Pengguna yang menerima SMS mencurigakan dan ingin memeriksa keamanannya sebelum merespons atau mengklik tautan.
- **Dosen & Tim Evaluator Akademik**: Menguji keandalan model ML, melihat visualisasi perbandingan algoritma, confusion matrix, dan pipeline data science.

### 2.2 Skenario Penggunaan Utama
- **Skenario 1 (Pemeriksaan Cepat Teks Tunggal)**: Pengguna menyalin teks SMS dari ponsel, menempelkannya ke kotak input web, memilih tombol "Periksa SMS", dan dalam waktu $< 1$ detik memperoleh hasil klasifikasi, tingkat risiko, dan saran tindak lanjut.
- **Skenario 2 (Uji Coba dengan Template Bawaan)**: Pengguna/dosen mengklik salah satu tombol contoh pesan (Normal, Promosi, Penipuan/Phishing) untuk langsung melihat respon aplikasi tanpa perlu mengetik manual.
- **Skenario 3 (Pemeriksaan Massal via Unggah CSV)**: Pengguna mengunggah file CSV berisi daftar SMS untuk diklasifikasikan secara kolektif, lalu mengunduh hasil prediksi berlabel.
- **Skenario 4 (Transparansi Model & Edukasi)**: Pengguna membuka tab "Tentang Model & Metrik" untuk meninjau tabel performa 3 algoritma (Accuracy, Precision, Recall, F1-Score) dan anatomi modus penipuan SMS.

---

## 3. Arsitektur Sistem & Alur Kerja (System Architecture & Pipeline)

Alur kerja aplikasi mengikuti kaidah resmi M15:
$$\text{Input Data} \longrightarrow \text{Preprocessing} \longrightarrow \text{Machine Learning Pipeline} \longrightarrow \text{Prediction \& Analysis} \longrightarrow \text{Interactive Result}$$

```
+-------------------------------------------------------------+
|                     PENGGUNA (WEB BROWSER)                  |
|  - Input Teks SMS / Upload CSV                              |
|  - Tombol Quick Examples (Normal, Promo, Penipuan)          |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     STREAMLIT APPLICATION                   |
|  1. Input Validation (Pengecekan teks kosong & batas input) |
|  2. Rule-Based Heuristic Parser (URL, Phone, Keyword check) |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     PREPROCESSING PIPELINE                  |
|  - Case Folding (lowercase)                                 |
|  - Regex Cleaning (pembersihan noise, URL placeholder)      |
|  - Slang Normalization (kamus kata singkatan SMS Indo)      |
|  - Tokenization                                             |
|  - TF-IDF Vectorizer (Unigram + Bigram, Sublinear TF)       |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     MACHINE LEARNING ENGINE                 |
|  Model Terlatih (Trained Model Artifacts / .pkl / .joblib): |
|   * Model 1: Multinomial Naive Bayes (Baseline)             |
|   * Model 2: Logistic Regression (Model Terpilih/Default)   |
|   * Model 3: Linear Support Vector Machine (Linear SVM)     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     HASIL PREDIKSI & VISUALISASI            |
|  - Status Label: Normal (Aman) / Promosi / Penipuan         |
|  - Probabilitas Keyakinan (Confidence Gauge / Bar Chart)    |
|  - Word Contribution / Influential Keywords (Interpretasi)  |
|  - Indikator Risiko Heuristik (Deteksi Tautan/No. Rekening) |
|  - Rekomendasi Tindakan Keamanan Pengguna                   |
+-------------------------------------------------------------+
```

---

## 4. Rincian Fitur Aplikasi (Functional Requirements)

### 4.1 Modul 1: Halaman Utama Deteksi SMS (Single SMS Scanner)
1. **Fitur Deteksi Bahasa Otomatis (Language Auto-Detection)**:
   - Sistem secara cerdas mendeteksi bahasa teks masukan: **Bahasa Indonesia** atau **English (Bahasa Inggris)** dengan tingkat keyakinan (*confidence score*).
   - Pengguna juga dapat memilih secara manual melalui pemilih bahasa (*Auto-Detect*, *Bahasa Indonesia*, *English*).
   - Preprocessing dan routing model menyesuaikan bahasa yang terdeteksi (menggunakan kamus slang dan pola tokenisasi yang sesuai).
2. **Input Teks SMS**:
   - Area teks interaktif (`st.text_area`) dengan placeholder informatif dwibahasa.
   - Penghitung karakter dan jumlah kata secara *real-time*.
   - Validasi input: memberikan peringatan ramah jika tombol "Periksa" ditekan saat kolom teks masih kosong atau hanya berisi spasi.
3. **Tombol Preset / Contoh SMS Cepat (One-Click Examples)**:
   - Disediakan contoh pesan instan untuk **Bahasa Indonesia** dan **English**:
     - *Contoh Normal ID/EN* (misal: "Besok kuliah jam 8..." / "Hey mate, are you coming tonight?").
     - *Contoh Promosi ID/EN* (misal: "[PROMO] Paket Flash..." / "Special offer 4u! Get video phone...").
     - *Contoh Penipuan ID/EN* (misal: "Selamat Cek Tunai 100jt..." / "URGENT! You won 1000 cash prize...").
4. **Hasil Klasifikasi Utama (Card Banner)**:
   - Menampilkan badge bahasa yang terdeteksi (🇮🇩 Bahasa Indonesia / 🇬🇧 English).
   - **Hijau (Normal / Ham)**: SMS teridentifikasi sebagai percakapan wajar/aman.
   - **Kuning / Oranye (Promosi / Marketing)**: SMS penawaran produk/layanan resmi operator.
   - **Merah (Indikasi Penipuan / Phishing)**: SMS berbahaya yang mengindikasikan rekayasa sosial, manipulasi, atau tautan phising.
5. **Probabilitas & Skor Keyakinan (Confidence Metrics)**:
   - Progress bar atau metric card yang menampilkan persentase keyakinan model (misal: Penipuan: 94.2%, Promosi: 4.1%, Normal: 1.7%).
6. **Analisis Indikator Heuristik (Risk Factor Badges)**:
   - Deteksi URL / Domain mencurigakan (misal: link shortener `bit.ly`, `tinyurl`, domain gratisan `blogspot`, `.xyz`).
   - Deteksi kontak nomor ponsel tidak resmi / WhatsApp pengirim.
   - Deteksi kata kunci manipulatif (*sense of urgency*, kata "Selamat", "Menang", "Rekening", "Hadiah", "Klaim", "Pinjaman").
6. **Interpretasi Kata Berpengaruh (Explainable Words)**:
   - Menampilkan kata-kata dalam pesan yang paling berkontribusi mendorong model ke label prediksi (berdasarkan bobot koefisien feature TF-IDF).
7. **Rekomendasi Tindakan Preventif**:
   - Tips keamanan yang relevan sesuai hasil (misal: "Jangan pernah mengklik tautan", "Jangan bagikan kode OTP", "Laporkan nomor ke 112 / aduankonten.id").

### 4.2 Modul 2: Pemeriksaan Massal (Batch Prediction via CSV Upload)
1. **Unggah File CSV**: Pengguna dapat mengunggah file `.csv` yang berisi kolom teks SMS.
2. **Pemetaan Kolom Otomatis**: Memilih kolom teks secara otomatis atau membiarkan pengguna memilih kolom teks yang ingin dianalisis.
3. **Batch Processing**: Menjalankan pipeline prediksi terhadap seluruh baris.
4. **Tabel Interaktif**: Menampilkan data dengan kolom tambahan: `Prediksi_Kategori`, `Probabilitas_Keyakinan`, dan `Status_Risiko`.
5. **Ringkasan Grafik**: Menampilkan pie chart / bar chart distribusi hasil prediksi pada batch tersebut.
6. **Ekspor Hasil**: Tombol unduh file CSV hasil prediksi (`Hasil_Deteksi_SMS.csv`).

### 4.3 Modul 3: Dashboard Evaluasi Model & Transparansi Akademik
1. **Ringkasan Dataset**:
   - Informasi volume data latih dan uji, sumber dataset (Dataset Yudi Wibisono 1.143 SMS & Dataset Phishing 1.772 teks), distribusi kelas awal.
2. **Tabel Perbandingan 3 Algoritma**:
   - Membandingkan **Multinomial Naive Bayes**, **Logistic Regression**, dan **Linear SVM** pada metrik:
     - Accuracy
     - Precision (Macro & per-kelas)
     - Recall (Macro & per-kelas, difokuskan pada Recall Penipuan)
     - F1-Score (Macro & per-kelas)
3. **Visualisasi Confusion Matrix**:
   - Heatmap matriks kebingungan untuk masing-masing model untuk menunjukkan tingkat kesalahan prediksi (*False Positive* & *False Negative*).
4. **Justifikasi Pemilihan Model Terbaik**:
   - Narasi ilmiah mengapa satu model tertentu dipilih sebagai default aplikasi (misal: Logistic Regression dipilih karena memberikan F1-Score tinggi, probabilitas terkalibrasi baik, dan minim resiko meloloskan SMS penipuan).

### 4.4 Modul 4: Panduan Edukasi Keamanan Siber (Security Anatomy)
1. Panduan mengenali taktik umum smishing di Indonesia:
   - Modus APK Kurir / Undangan Pernikahan.
   - Modus Menang Undian Marketplace / Bank.
   - Modus Tagihan Ilegal & Pinjol Cepat Cair.
2. Daftar nomor dan kontak resmi pengaduan penipuan di Indonesia (Kominfo, OJK, Patroli Siber Polri).

---

## 5. Kebutuhan Non-Fungsional (Non-Functional Requirements)

1. **Kecepatan & Latensi (Performance)**:
   - Waktu respons inferensi model untuk 1 SMS $\le 300\text{ ms}$.
   - Waktu proses batch 100 baris CSV $\le 3\text{ detik}$.
2. **Privasi Data Pengguna (Privacy & Safety)**:
   - Tidak ada penyimpanan/perekaman teks SMS masukan ke database atau disk (stateless processing by default) demi menjaga kerahasiaan data pribadi pengguna.
   - Tautan/URL yang terdeteksi di dalam teks tidak boleh dibuat menjadi tautan aktif (*non-clickable*) untuk mencegah pengguna salah klik tautan berbahaya secara tidak sengaja.
3. **Portabilitas & Reproduksibilitas (Reproducibility)**:
   - Menggunakan format serialisasi model standar (`joblib` / `pickle`).
   - Seluruh dependensi didefinisikan dalam `requirements.txt`.
   - Kode dapat dijalankan dengan perintah sederhana: `streamlit run app.py`.
4. **Tampilan Antarmuka (UI/UX)**:
   - Desain bersih, modern, dan intuitif menggunakan tema bawaan Streamlit yang dioptimasi dengan elemen Markdown interaktif.
   - Responsif pada tampilan desktop maupun perangkat bergerak (smartphone).

---

## 6. Rencana Dataset & Spesifikasi Modeling

### 6.1 Dataset yang Digunakan
1. **Dataset Primer (3-Kelas SMS Indonesia)**:
   - Berkas: `Project/Indonesia/dataset_sms_spam_v1.csv`
   - Sumber: Korpus Riset SMS Bahasa Indonesia (Yudi Wibisono, 2018; banyak dirujuk jurnal SINTA).
   - Ukuran: 1.143 baris pesan SMS nyata.
   - Label:
     - `0` = **Normal / Ham** (569 data / ~49.8%)
     - `1` = **Penipuan / Smishing / Fraud** (335 data / ~29.3%)
     - `2` = **Promosi / Operator / Spam Iklan** (239 data / ~20.9%)
2. **Dataset Sekunder / Validasi Tambahan (Phishing SMS & Email Indo)**:
   - Berkas: `Project/Indonesia/dataset_phishing_sms_indo.csv` (1.772 pesan, label biner & anotasi sub-kategori seperti minta_data, urgensi, berhadiah).
   - Digunakan untuk pengujian generalisasi pola phishing modern dan perbendaharaan kata pemicu heuristik.

### 6.2 Preprocessing Pipeline
1. **Cleaning**: Mengubah huruf kecil (*case folding*), menghapus tag XML/HTML, normalisasi spasi.
2. **Entity Token Masking**:
   - URL disamarkan menjadi token `[URL]`.
   - Nomor telepon/kontak disamarkan menjadi token `[NOMOR]`.
   - Nilai nominal rupiah disamarkan menjadi token `[NOMINAL]`.
3. **Slang / Abbreviation Normalization**:
   - Memetakan singkatan umum SMS Indonesia (misal: `dpt` $\rightarrow$ `dapat`, `sy` $\rightarrow$ `saya`, `hub` $\rightarrow$ `hubungi`, `rek` $\rightarrow$ `rekening`, `bca` $\rightarrow$ `bank`, `jt` $\rightarrow$ `juta`).
4. **Vectorization**:
   - `TfidfVectorizer(ngram_range=(1, 2), max_features=3000, sublinear_tf=True)`.

### 6.3 Algoritma Pembanding (Wajib $\ge 3$)
1. **Multinomial Naive Bayes (MNB)**:
   - Alasan: Algoritma teks klasik berkecepatan tinggi, bekerja efektif pada data frekuensi kata diskrit.
2. **Logistic Regression (LR)**:
   - Alasan: Model linear dengan regularisasi ($L_2$), tahan terhadap *overfitting* pada dimensi teks tinggi, menghasilkan probabilitas kelas terkalibrasi dengan baik.
3. **Linear Support Vector Machine (Linear SVM / SGDClassifier)**:
   - Alasan: Sangat unggul dalam menemukan *hyperplane* pemisah optimal pada ruang vektor fitur teks yang renggang (*sparse text space*).

### 6.4 Strategi Evaluasi
- **Pembagian Data**: $80\%$ Training dan $20\%$ Testing dengan teknik **Stratified Split** untuk menjaga keseimbangan proporsi kelas pada train dan test.
- **Validasi Internal**: Stratified 5-Fold Cross Validation pada subset training.
- **Metrik Utama**:
  - Prioritas 1: **Recall pada Kelas Penipuan** (Meminimalkan *False Negative*, yaitu SMS penipuan berbahaya yang lolos dan dikira SMS normal).
  - Prioritas 2: **Macro-Averaged F1-Score** (Mengukur keseimbangan performa ketiga kelas secara adil tanpa terdistorsi kelas dominan).
  - Prioritas 3: **Accuracy & Confusion Matrix**.

---

## 7. Roadmap & Kriteria Keberhasilan (Acceptance Criteria)

| Fase | Target Luaran | Kriteria Selesai |
|---|---|---|
| **Fase 1: PRD & Perencanaan** | Dokumen PRD.md & Project.md | Tersusun lengkap di folder `project`, memetakan semua poin rubrik M15 |
| **Fase 2: Eksplorasi & Preprocessing** | Skrip EDA & Preprocessing Pipeline | Terbentuk visualisasi distribusi data, teks bersih, dan normalisasi singkatan |
| **Fase 3: Model Training & Benchmark** | Model `.joblib` & Tabel Evaluasi | 3 Algoritma terlatih, tabel metrik perbandingan & confusion matrix tersimpan |
| **Fase 4: Pengembangan Web Streamlit** | Aplikasi Web `app.py` | Berjalan lancar, mendukung input tunggal, preset contoh, upload CSV, dan visualisasi |
| **Fase 5: Dokumentasi, PPT & Video Demo** | Slide Presentasi & Naskah Video $\le 7$ mnt | Siap presentasi dan demo langsung sesuai format pengumpulan |

---
*Dokumen ini merupakan panduan resmi pengembangan produk di folder `project`.*

