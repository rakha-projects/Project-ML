# M15 - Project dan Refleksi: Deskripsi Project

Project akhir Mata Kuliah **Pembelajaran Mesin (Machine Learning)** dirancang untuk memberikan pengalaman kepada mahasiswa dalam menerapkan konsep, metode, dan algoritma Machine Learning untuk menyelesaikan permasalahan nyata berbasis data.

Setiap kelompok akan mengembangkan suatu model Machine Learning mulai dari tahapan identifikasi masalah, pengumpulan atau pemilihan dataset, eksplorasi data, preprocessing, pembangunan model, evaluasi, hingga implementasi model dalam bentuk aplikasi sederhana yang dapat digunakan oleh pengguna.

Mahasiswa diharapkan tidak hanya mampu menghasilkan model dengan performa yang baik, tetapi juga mampu menjelaskan alasan pemilihan metode, melakukan evaluasi model secara tepat, serta menginterpretasikan hasil yang diperoleh.

### Hasil Akhir Project:
- Model Machine Learning yang telah dilatih dan dievaluasi.
- Aplikasi / interface sederhana untuk menjalankan model.
- Source code project.
- PPT laporan project.
- Video demo aplikasi.

---

## 1. Ketentuan Kelompok
- Setiap kelompok terdiri dari **3 orang mahasiswa**.
- Setiap anggota kelompok harus memiliki pembagian tugas yang jelas.
- Seluruh anggota wajib memahami konsep, dataset, metode, algoritma, serta implementasi project yang dikerjakan.
- **Nilai pengerjaan project** merupakan nilai kelompok.
- **Nilai presentasi dan tanya jawab** merupakan nilai individu.
- Setiap anggota kelompok wajib dapat menjelaskan bagian project yang dikerjakan maupun konsep utama project secara keseluruhan.

---

## 2. Tema Project
Setiap kelompok dapat memilih permasalahan yang dapat diselesaikan menggunakan pendekatan Machine Learning. Tema yang dapat dipilih antara lain:

### A. Classification
Membangun model untuk memprediksi kategori atau kelas tertentu.  
**Contoh:**
- Prediksi kelayakan kredit.
- Prediksi mahasiswa berisiko tidak lulus tepat waktu.
- Klasifikasi kualitas produk.
- Prediksi pelanggan *churn*.
- Klasifikasi tingkat risiko penyakit berdasarkan data.
- Deteksi transaksi mencurigakan.
- Klasifikasi kualitas pangan berdasarkan karakteristik fisik atau kimia.

### B. Regression
Membangun model untuk memprediksi nilai numerik/kontinu.  
**Contoh:**
- Prediksi harga rumah.
- Prediksi hasil produksi pertanian.
- Prediksi konsumsi energi.
- Prediksi nilai penjualan.
- Prediksi suhu atau parameter lingkungan.
- Prediksi kualitas produk berdasarkan parameter proses.

### C. Clustering
Mengelompokkan data berdasarkan kemiripan karakteristik tanpa label kelas.  
**Contoh:**
- Segmentasi pelanggan.
- Pengelompokan pola konsumsi.
- Pengelompokan wilayah berdasarkan parameter lingkungan.
- Pengelompokan produk berdasarkan karakteristik.
- Pengelompokan mahasiswa berdasarkan pola akademik.

### D. Anomaly Detection
Mengidentifikasi data atau kondisi yang berbeda secara signifikan dari pola normal.  
**Contoh:**
- Deteksi anomali sensor.
- Deteksi kerusakan mesin.
- Deteksi transaksi tidak normal.
- Deteksi kondisi produksi yang tidak normal.
- Deteksi penyimpangan kualitas produk.

### E. Time Series / Forecasting
Membangun model untuk melakukan prediksi berdasarkan data runtun waktu.  
**Contoh:**
- Prediksi penjualan.
- Prediksi konsumsi listrik.
- Prediksi suhu.
- Prediksi jumlah produksi.
- Prediksi permintaan produk.

### F. Recommendation System
Membangun sistem yang dapat memberikan rekomendasi berdasarkan karakteristik pengguna atau data historis.  
**Contoh:**
- Rekomendasi produk.
- Rekomendasi makanan.
- Rekomendasi film.
- Rekomendasi buku.
- Rekomendasi pilihan berdasarkan karakteristik pengguna.

### G. Topik Lain
Topik lain diperbolehkan selama memenuhi syarat:
- Menggunakan konsep Machine Learning.
- Memiliki dataset yang dapat dianalisis.
- Memiliki permasalahan yang jelas.
- Memiliki metode evaluasi yang terukur.
- Mendapatkan persetujuan dosen pengampu.

---

## 3. Pengajuan Tema Project
Pada saat mengajukan tema project, setiap kelompok wajib menyampaikan:
1. Judul project.
2. Latar belakang singkat.
3. Permasalahan yang ingin diselesaikan.
4. Tujuan project.
5. Dataset yang akan digunakan.
6. Sumber dataset.
7. Variabel / feature yang digunakan.
8. Target / output yang akan diprediksi atau dianalisis.
9. Algoritma Machine Learning yang direncanakan.
10. Minimal **5 artikel jurnal ilmiah** yang relevan dengan project.

> **Fungsi Artikel Jurnal:**  
> Artikel jurnal digunakan sebagai referensi dalam menentukan:
> - Permasalahan penelitian
> - Dataset / variabel
> - Metode preprocessing
> - Algoritma Machine Learning
> - Metode evaluasi model

Kelompok juga wajib membuat **tabel studi literatur** dengan format berikut:

| No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Project |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | ... | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... | ... | ... |

---

## 4. Dataset

### Sumber Dataset
Dataset dapat berasal dari:
- Kaggle
- UCI Machine Learning Repository
- Data Pemerintah / Open Data
- Dataset penelitian
- Dataset hasil pengukuran sendiri
- Dataset dari sensor / IoT
- Dataset institusi yang diperbolehkan digunakan
- Sumber dataset terbuka lainnya

> [!IMPORTANT]
> - Dataset harus memiliki sumber yang jelas.
> - Dilarang menggunakan dataset tanpa memahami arti masing-masing variabel.

### Karakteristik yang Wajib Dijelaskan:
- Jumlah data.
- Jumlah feature/variabel.
- Tipe data.
- Target/label (apabila menggunakan supervised learning).
- Distribusi data.
- Missing value.
- Outlier.
- Ketidakseimbangan kelas (apabila ditemukan).
- Proses pembersihan/preprocessing yang dilakukan.

---

## 5. Eksplorasi Data / Exploratory Data Analysis (EDA)
Sebelum membuat model, mahasiswa wajib melakukan analisis awal terhadap dataset.

### Cakupan Minimal EDA:
- Informasi umum dataset.
- Statistik deskriptif.
- Pemeriksaan missing value.
- Pemeriksaan data duplikat.
- Pemeriksaan outlier (jika relevan).
- Distribusi variabel.
- Distribusi kelas/target.
- Korelasi antarvariabel (apabila relevan).
- Visualisasi data yang mendukung analisis.

### Contoh Visualisasi:
- Histogram
- Bar chart
- Boxplot
- Scatter plot
- Correlation matrix / heatmap
- Grafik distribusi kelas

> [!NOTE]
> Setiap visualisasi harus dijelaskan maknanya, bukan hanya sekadar ditampilkan.

---

## 6. Preprocessing Data
Kelompok wajib menjelaskan setiap tahap preprocessing yang dilakukan. Preprocessing dapat meliputi:
- Data cleaning
- Penanganan missing value
- Penghapusan data duplikat
- Penanganan outlier
- Encoding data kategorikal
- Normalization & Standardization
- Feature selection & Feature engineering
- Penanganan class imbalance
- Pembagian data training dan testing

> [!TIP]
> Tidak seluruh preprocessing harus digunakan. Gunakan preprocessing yang memang diperlukan oleh karakteristik dataset dan algoritma yang dipilih.

---

## 7. Pengembangan Model Machine Learning
Setiap kelompok wajib menggunakan **minimal 3 algoritma/model** untuk dibandingkan.

### Contoh Algoritma:
- **Classification**: Logistic Regression, K-Nearest Neighbors (KNN), Decision Tree, Random Forest, Support Vector Machine (SVM), Naive Bayes, Gradient Boosting, XGBoost, dll.
- **Regression**: Linear Regression, Polynomial Regression, Decision Tree Regression, Random Forest Regression, Support Vector Regression (SVR), Gradient Boosting Regression, dll.
- **Clustering**: K-Means, Hierarchical Clustering, DBSCAN, dll.

> [!WARNING]
> Pemilihan algoritma harus memiliki alasan ilmiah yang jelas, tidak hanya mencoba-coba algoritma secara acak.

---

## 8. Training dan Testing
Dataset harus dibagi secara tepat menjadi data training dan testing.
- **Contoh pembagian:** `80% training : 20% testing` (atau rasio lain yang dapat dipertanggungjawabkan).

### Teknik Tambahan (Jika Diperlukan):
- Train-validation-test split
- K-Fold Cross Validation / Stratified K-Fold
- Hyperparameter tuning (Grid Search, Randomized Search, dll.)

> [!CAUTION]
> Mahasiswa wajib memastikan bahwa **data testing tidak digunakan** dalam proses training model untuk mencegah terjadinya *data leakage*.

---

## 9. Evaluasi Model
Metrik evaluasi harus disesuaikan dengan jenis permasalahan:

- **Classification**:
  - *Minimal:* Accuracy, Precision, Recall, F1-Score, Confusion Matrix.
  - *Tambahan:* ROC Curve, AUC, Specificity.
- **Regression**:
  - *Minimal:* MAE, MSE, RMSE, R².
- **Clustering**:
  - Silhouette Score, Davies-Bouldin Index, Elbow Method, Evaluasi visual cluster.

### Perbandingan Model
Kelompok wajib membandingkan performa seluruh model yang digunakan dalam bentuk tabel.

**Contoh Format Perbandingan (Classification):**

| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| Model 1 | ... | ... | ... | ... |
| Model 2 | ... | ... | ... | ... |
| Model 3 | ... | ... | ... | ... |

> Kelompok harus menjelaskan alasan mengapa satu model tertentu dipilih untuk diimplementasikan ke aplikasi berdasarkan hasil evaluasi.

---

## 10. Analisis Model
Kelompok tidak diperbolehkan hanya menyampaikan angka metrik evaluasi tanpa analisis. Wajib terdapat pembahasan mengenai:
- Model dengan performa terbaik dan terendah.
- Kemungkinan penyebab perbedaan performa antar model.
- Identifikasi apakah terjadi *overfitting* atau *underfitting*.
- Analisis kesalahan prediksi model (*error analysis*).
- Faktor/feature yang paling berpengaruh (*feature importance*).
- Keterbatasan model.
- Potensi pengembangan model selanjutnya.

---

## 11. Output Project
Output utama project adalah **aplikasi berbasis Machine Learning** yang dapat digunakan secara interaktif oleh pengguna.

### Bentuk Aplikasi & Rekomendasi Teknologi:
- **Bentuk:** Web application, Desktop application, Mobile application, Dashboard interaktif.
- **Teknologi:** Streamlit, Gradio, Flask, FastAPI, Django, atau teknologi lain yang sesuai.

### Alur Kerja Aplikasi:
$$\text{Input Data} \longrightarrow \text{Preprocessing} \longrightarrow \text{Machine Learning Model} \longrightarrow \text{Prediction} \longrightarrow \text{Result}$$

1. **Input:** Pengguna dapat memasukkan data yang diperlukan model (angka, data kategorikal, upload CSV, data sensor, dll.).
2. **Process:** Aplikasi menjalankan model Machine Learning dan alur prediksi.
3. **Output:** Menampilkan hasil prediksi secara jelas (kelas, nilai numerik, probabilitas, cluster, status anomali, visualisasi/grafik, dll.).

---

## 12. Source Code
Source code project harus tersusun rapi, terdokumentasi, dan dapat direproduksi (*reproducible*).

### Komponen Minimal Source Code:
1. Proses loading dataset
2. EDA (Exploratory Data Analysis)
3. Preprocessing data
4. Training model
5. Evaluasi model
6. Perbandingan model
7. Penyimpanan model (*export/dump model*)
8. Implementasi aplikasi

### Media / Format Pengerjaan:
- Jupyter Notebook (`.ipynb`)
- Google Colab
- Python script (`.py`)
- GitHub Repository

> [!NOTE]
> Kode harus dilengkapi dengan komentar / penjelasan seperlunya agar alur logika mudah dipahami.

---

## 13. Video Demo Aplikasi
Setiap kelompok wajib membuat video demo presentasi aplikasi dengan ketentuan:
- ⏱️ **Durasi maksimal: $\le$ 7 menit**

### Muatan Minimal Video:
1. Perkenalan anggota kelompok
2. Judul project
3. Latar belakang masalah
4. Dataset yang digunakan
5. Tahapan preprocessing
6. Algoritma Machine Learning yang digunakan
7. Perbandingan performa model
8. Model terbaik yang dipilih
9. Demonstrasi aplikasi secara langsung (*live execution*)
10. Kesimpulan

> [!IMPORTANT]
> Video harus memperlihatkan aplikasi **benar-benar dijalankan**, bukan sekadar presentasi tangkapan layar (*screenshot*).

---

## 14. Laporan Project (PPT)
Laporan project dibuat dalam bentuk **file presentasi (PPT)** yang digunakan untuk presentasi dan video demo project.

### Struktur Minimal PPT:
- **A. Judul Project**: Judul, nama anggota, NIM, dan kelas.
- **B. Latar Belakang & Masalah**: Kondisi/masalah, alasan pemilihan, dan signifikansi penyelesaian.
- **C. Tujuan Project**: Target capaian project.
- **D. Studi Literatur**: Ringkasan minimal 5 artikel jurnal terkait.
- **E. Dataset**: Sumber, volume data, fitur, target, dan karakteristik data.
- **F. Exploratory Data Analysis**: Hasil analisis dan visualisasi utama.
- **G. Preprocessing**: Rincian tahapan pra-pemrosesan data.
- **H. Pengembangan Model**: Algoritma, rasio split train/test, parameter, dan proses training.
- **I. Evaluasi dan Perbandingan Model**: Tabel/grafik hasil evaluasi seluruh model.
- **J. Pemilihan Model Terbaik**: Justifikasi pemilihan model terpilih.
- **K. Implementasi Aplikasi**: Arsitektur sistem, teknologi, alur input-proses-output.
- **L. Demo Project**: Dokumentasi alur pengoperasian aplikasi.
- **M. Kesimpulan**: Ringkasan temuan utama project.
- **N. Keterbatasan dan Pengembangan**: Batasan dataset/model/aplikasi dan saran riset lanjutan.
- **O. Pembagian Tugas**:

| Anggota | Rincian Tugas |
| :--- | :--- |
| **Mahasiswa 1** | Dataset, EDA, Data Preprocessing |
| **Mahasiswa 2** | Modeling dan Evaluasi Model |
| **Mahasiswa 3** | Implementasi Aplikasi dan Deployment |

*(Tabel di atas hanya contoh pembagian peran. Seluruh anggota tetap wajib memahami keseluruhan alur project).*

---

## 15. Penilaian Project

### Komponen Penilaian Kelompok

| Komponen | Bobot |
| :--- | :---: |
| Identifikasi masalah & studi literatur | 10% |
| Dataset, EDA & preprocessing | 15% |
| Pengembangan model Machine Learning | 20% |
| Evaluasi & analisis model | 20% |
| Implementasi aplikasi | 15% |
| PPT & video demo | 10% |
| Originalitas / inovasi project | 5% |
| Pembagian tugas & kualitas dokumentasi | 5% |
| **TOTAL** | **100%** |

### Penilaian Individu
Dilakukan sesi **tanya jawab individu** untuk menguji pemahaman masing-masing mahasiswa terhadap:
- Pemahaman konsep dasar Machine Learning.
- Pemahaman dataset dan perilakunya.
- Pemahaman teknik preprocessing yang diterapkan.
- Pemahaman algoritma yang dipilih.
- Kemampuan membaca dan menginterpretasikan hasil evaluasi.
- Kemampuan menjelaskan baris kode dan implementasinya.
- Kemampuan menjelaskan arsitektur aplikasi.

---

## 16. Ketentuan Penting
1. **Transparansi Data:** Dataset dan sumber data wajib dicantumkan dengan jelas.
2. **Orisinalitas:** Dilarang keras menggunakan atau menjiplak project milik kelompok lain.
3. **Integritas Teknis:** Tidak boleh sekadar mengunduh source code dari internet tanpa memahami proses dan logikanya.
4. **Etika Penggunaan AI:** Penggunaan AI / Generative AI diperbolehkan sebatas alat bantu belajar dan debugging; mahasiswa bertanggung jawab penuh atas pemahaman kode dan analisis.
5. **Kesiapan Demo:** Setiap kelompok harus siap menjalankan kembali aplikasinya secara langsung saat sesi presentasi.
6. **Validitas Hasil:** Seluruh hasil evaluasi harus murni berasal dari eksperimen pengujian model nyata.
7. **Justifikasi Pilihan:** Mahasiswa wajib mampu menjelaskan alasan pemilihan setiap preprocessing, algoritma, dan metrik evaluasi.
8. **Prinsip Evaluasi:** Model dengan akurasi tertinggi tidak otomatis menjadi model terbaik; evaluasi harus disesuaikan dengan konteks permasalahan (misal: F1-score/Recall pada imbalanced data).
9. **Rencana Cadangan:** Apabila aplikasi mengalami kendala saat presentasi, kelompok tetap wajib menjelaskan penyebab teknis serta menunjukkan dokumentasi pengujian dan kodenya.

---

## 17. Pengumpulan Berkas

### Berkas yang Wajib Dikumpulkan:
1. File PPT Laporan Project
2. Source Code / Tautan GitHub Repository
3. Dataset atau tautan unduhan dataset
4. Model terlatih (*trained model weights/pickle*), jika relevan
5. Video Demo Aplikasi (maksimal 7 menit)
6. Daftar 5 Jurnal Referensi
7. Tabel Studi Literatur
8. Tautan Aplikasi / Deployment (jika online)

### Format Penamaan Folder:
```text
ML2026_Kelas_NamaKelompok_JudulProject
```
**Contoh:**
```text
ML2026_A_Kelompok03_PrediksiKualitasAir
```

---

## 🏆 Reward Project Terbaik

> [!TIP]
> ### 🌟 **NILAI UAS TEORI = 100**
> 
> **Ketentuan:**
> - Dipilih **1 kelompok terbaik per kelas**.
> - Kelompok terbaik **tetap wajib hadir** pada jadwal pelaksanaan UAS resmi sesuai ketentuan akademik untuk memenuhi presensi dan tanda tangan kehadiran.
