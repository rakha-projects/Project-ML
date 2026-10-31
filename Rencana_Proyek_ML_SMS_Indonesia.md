# Rencana proyek ML: pemeriksa SMS berbahasa Indonesia

**Status:** rencana pengajuan, belum implementasi dan belum mengunci dataset.  
**Rujukan ketentuan:** M15 – Project dan Refleksi, dokumen tugas yang diberikan dosen.  
**Tanggal penelusuran sumber:** 27 Oktober 2026.

## 1. Ringkasan dan keputusan awal

**Judul kerja:** *Perbandingan Algoritma Machine Learning untuk Klasifikasi SMS Berbahasa Indonesia dan Implementasinya pada Web Interaktif*.

Web dibuat dengan Streamlit. Pengguna menempel teks SMS, menekan tombol periksa, dan memperoleh kategori serta penjelasan ringkas. Kategori final mengikuti **label asli dataset yang dipilih**. Target yang diinginkan adalah **Normal, Promosi, dan Indikasi Penipuan**; jika dataset lebih baru hanya memiliki label spam/non-spam, judul, tujuan, dan keluaran harus diubah menjadi dua kelas. Jangan mengganti nama label tanpa audit dan pelabelan ulang.

Ruang lingkup ini adalah **klasifikasi teks SMS**, bukan verifikasi identitas pengirim, pemeriksaan keamanan tautan secara langsung, atau akses otomatis ke kotak SMS pengguna. Prediksi adalah indikasi untuk membantu pengguna memeriksa pesan.

## 2. Pemetaan ketentuan dosen ke rencana pengerjaan

| Ketentuan | Pekerjaan yang direncanakan | Bukti yang harus tersedia |
|---|---|---|
| Kelompok 3 orang; semua memahami proyek | Tetapkan penanggung jawab utama untuk data, pemodelan, dan web; lakukan tinjauan silang | Tabel pembagian tugas dan kesiapan tanya jawab setiap anggota |
| Tema dan pengajuan | Ajukan judul, latar belakang, masalah, tujuan, dataset, sumber, fitur, target, tiga algoritma, lima jurnal, tabel studi literatur | Formulir/ringkasan pengajuan tema |
| Sumber dan pemahaman dataset | Catat pembuat, lokasi unduh, lisensi, cara pengumpulan, bahasa, tanggal pembuatan/unggah, kolom, label, dan jumlah pesan | Kartu dataset dan audit berkas asli |
| EDA | Tampilkan distribusi kelas, panjang pesan, pesan kosong/duplikat, indikasi URL/nomor, serta kata/frasa per kelas | Notebook/grafik yang masing-masing dijelaskan |
| Preprocessing | Normalisasi seperlunya, pemeriksaan duplikat, pembagian data, TF-IDF hanya dipelajari dari data latih; eksperimen pilihan kata dan karakter | Pipeline yang dapat dijalankan ulang |
| Minimal 3 algoritma | Multinomial Naive Bayes, Logistic Regression, Linear SVM | Tabel alasan, parameter, dan hasil tiga model |
| Training dan testing | Data uji terpisah; validasi/tuning di bagian latih; cegah pesan identik atau hampir identik menyeberang split | Proporsi split, seed, dan prosedur validasi |
| Evaluasi dan analisis | Accuracy, precision, recall, F1 per kelas, macro-F1, confusion matrix; cek train vs validasi, contoh salah prediksi, alasan pemilihan model | Tabel perbandingan dan analisis kesalahan |
| Aplikasi ML | Web Streamlit dengan Input → Preprocessing → Model → Prediction → Result | Demo web berjalan, bukan tangkapan layar |
| Source code | Notebook/skrip EDA, training, evaluasi, penyimpanan pipeline, dan web | Repositori dengan README dan dependencies |
| PPT dan video | PPT semua bagian yang diminta; video demo maksimal 7 menit | PPT final dan video aplikasi benar-benar dijalankan |
| Literatur | Minimal 5 artikel **jurnal ilmiah** relevan, dengan tabel studi literatur | Lima artikel terverifikasi dan tabel lengkap |

Ketentuan **tidak menyatakan dataset harus terbaru atau ide harus belum pernah dibuat**. Kebaruan dataset adalah preferensi proyek, bukan syarat tertulis. Contoh persentase bobot penilaian yang pernah beredar tidak tercantum dalam dokumen ketentuan ini.

## 3. Latar belakang, masalah, tujuan

**Latar belakang.** SMS normal, promosi, dan pesan yang terindikasi penipuan dapat tampak mirip bagi pengguna. Pemeriksaan berbasis teks dapat membantu memilah pesan sebelum pengguna mengambil tindakan.

**Pertanyaan proyek:** seberapa baik tiga algoritma klasifikasi teks membedakan kategori pesan pada dataset Indonesia yang dapat dipertanggungjawabkan, dan bagaimana hasilnya disajikan lewat web secara jelas?

**Tujuan:** (1) membangun pipeline klasifikasi SMS bahasa Indonesia; (2) membandingkan minimal tiga algoritma pada evaluasi yang sama; (3) menganalisis kesalahan, khususnya pesan penipuan yang salah diprediksi normal; (4) mengimplementasikan model terpilih pada web Streamlit.

**Batasan:** prediksi hanya berdasarkan teks yang ditempel; tidak mengesahkan bahwa pesan/pengirim benar-benar aman atau jahat. Bahasa gaul, ejaan yang disamarkan, dan modus baru perlu diuji secara terpisah.

## 4. Penelusuran dataset Indonesia yang lebih baru

| Kandidat | Yang dapat dipastikan dari sumber | Keputusan untuk saat ini |
|---|---|---|
| [Yudi Wibisono, publikasi 2018](https://yudiwbs.wordpress.com/2018/08/05/dataset-klasifikasi-bahasa-indonesia-sms-spam-klasifikasi-teks-dengan-scikit-learn/) | Sumber asli menjelaskan 1.143 SMS bahasa Indonesia dengan label normal, promosi, penipuan; dataset mahasiswa dipublikasikan dengan izin dan lisensi Creative Commons. | **Cadangan paling kuat untuk target tiga kelas.** Usia pesan lama; uji pesan kontemporer secara terpisah. |
| [GitHub phishing SMS Indonesia, unggahan yang ditemukan 2026](https://github.com/rasen-kurniawan/phishing-detection-eda) | Repositori memuat CSV dan menyebut 1.772 pesan untuk EDA phishing versus normal. | **Kandidat baru, belum layak dikunci** sampai asal pesan, tanggal pengumpulan, izin, cara pelabelan, dan duplikasi terhadap korpus lama diverifikasi. Labelnya dua kelas. |
| [SpamShield Multilingual, 2026](https://huggingface.co/datasets/M-Arjun/SpamShield-Datasets) | Kartu dataset menyebut subset Indonesia 1.270 pesan, 635 ham dan 635 spam; komposisi keseluruhan menyebut 20% augmentasi sintetis. Akses melalui permintaan otomatis. | **Alternatif dua kelas, bukan dataset tiga kelas.** Perlu audit sumber/proporsi sintetis khusus subset Indonesia dan cocok tidaknya untuk SMS penipuan. |
| [IndoTRUE-Net, 2026](https://zenodo.org/records/22092956) | 15.000 rekaman media sosial Indonesia dengan kelas spam, ham, uncertain. | **Tidak dipilih sebagai dataset utama**: domainnya media sosial, bukan SMS; uncertain bukan penipuan. |
| [Penelitian hadiah digital, 2026](https://journal.admi.or.id/index.php/JTS/article/view/2948) | Artikel melaporkan 6.000 pesan Indonesia, dua kelas, dianotasi dua orang. | **Literatur relevan; dataset belum terverifikasi tersedia untuk diunduh.** Jangan menganggap artikel otomatis menyediakan CSV. |

**Keputusan sementara:** jangan memilih dataset hanya karena tahun unggah 2026. Hingga pemeriksaan ini, kandidat yang **jelas sumbernya sekaligus pas dengan tiga label** masih dataset Yudi. Pencarian dataset lebih baru tetap terbuka. Jika kandidat 2026 lolos audit tetapi hanya biner, pilih secara sadar antara (A) mengubah proyek menjadi dua kelas atau (B) menambah pelabelan manual yang terdokumentasi; jangan memetakan spam menjadi penipuan.

**Pembedaan penting terkait SpamShield:** [halaman model SpamShield](https://huggingface.co/M-Arjun/SpamShield) menyebut model pralatih untuk beberapa bahasa (metadata menulis 7; kartu model menulis 8), sedangkan **datasetnya** mencakup 23 bahasa. Kartu model hanya menampilkan metrik per bahasa untuk delapan bahasa dan **tidak menampilkan evaluasi bahasa Indonesia**. Karena itu, keberadaan 1.270 pesan Indonesia dalam dataset tidak membuktikan model siap pakainya akurat untuk SMS Indonesia. Bila dataset tersebut dipakai, kelompok harus melatih dan menguji modelnya sendiri pada subset yang dipilih, sesuai kewajiban perbandingan minimal tiga algoritma.

**Pemeriksaan wajib sebelum dataset dikunci:** (1) unduh berkas yang sebenarnya; (2) hitung jumlah baris dan label dari berkas, bukan dari deskripsi; (3) periksa sampel tiap kelas; (4) catat sumber dan lisensi; (5) cek duplikat dengan dataset lama; (6) cek apakah teks hasil terjemahan/AI; (7) putuskan target final. Jika mengumpulkan pesan baru, hapus identitas pribadi, dapatkan izin yang sesuai, beri pedoman label, dan jadikan sebagai uji eksternal terpisah bila jumlahnya kecil.

## 5. Rancangan dataset, fitur, dan label

- **Unit analisis:** satu SMS = satu baris.
- **Masukan inti model:** isi teks SMS. Jangan memakai fitur yang tidak tersedia saat pengguna mengetik pesan pada web.
- **Label utama yang direncanakan:** normal, promosi, penipuan; berlaku hanya bila dataset final memang menyediakan atau telah diaudit untuk tiga kelas itu.
- **Fitur turunan untuk EDA/opsional eksperimen:** panjang karakter, jumlah kata, keberadaan URL, nomor, dan simbol tertentu. Ekstraksi harus identik pada data latih dan input web; jangan mengklaim fitur ini membuktikan adanya ancaman.
- **Data dictionary:** dokumentasikan makna setiap kolom dan setiap label. Jumlah, distribusi, missing value, duplikat, dan panjang pesan final diisi setelah audit berkas.

## 6. Rencana EDA dan preprocessing

1. Periksa skema, jumlah pesan, tipe kolom, label tidak sah, kosong, duplikat persis, dan pesan sangat mirip.
2. Buat grafik batang distribusi kelas; histogram/boxplot panjang pesan per kelas; perbandingan frekuensi URL/nomor; frasa yang menonjol per kelas. Jelaskan arti setiap grafik. Korelasi numerik hanya bila fitur numerik relevan.
3. Tetapkan aturan duplikat sebelum split agar versi pesan yang sama tidak masuk latih dan uji.
4. Pisahkan train/test terstratifikasi, misalnya 80/20, setelah audit duplikat. Gunakan Stratified K-Fold pada train untuk membandingkan dan menyesuaikan model.
5. Di dalam pipeline, rapikan huruf/spasi dan representasikan teks dengan TF-IDF. Bandingkan token kata dengan n-gram karakter jika waktu cukup; pertahankan sinyal seperti URL dan nomor dalam bentuk token pengganti. Stemming dan penghapusan stopword adalah eksperimen, bukan kewajiban otomatis.
6. Jika kelas timpang, nilai metrik per kelas dan pertimbangkan pembobotan kelas pada model yang mendukung; data uji tetap pada distribusi aslinya.

## 7. Eksperimen dan aturan memilih model

| Algoritma | Peran | Parameter yang layak diuji |
|---|---|---|
| Multinomial Naive Bayes | Baseline kuat dan cepat untuk teks | alpha |
| Logistic Regression | Pembanding linear dan penjelasan kontribusi fitur | C, class_weight |
| Linear SVM | Pembanding linear pada fitur teks jarang | C, class_weight |

**Aturan perbandingan:** ketiganya memakai split dan representasi fitur yang sama dalam percobaan utama. Pilih model dari validasi berdasarkan **macro-F1** dan **recall kelas penipuan**, sambil memeriksa precision agar alarm palsu tidak berlebihan. Gunakan test set sekali untuk pelaporan akhir, bukan untuk terus memilih parameter. Laporkan accuracy, precision/recall/F1 tiap kelas, macro-F1, confusion matrix, perbandingan train-validasi, dan contoh error yang dianonimkan.

Jika Linear SVM terpilih, jangan menampilkan skor marginnya sebagai probabilitas. Angka probabilitas hanya ditampilkan jika metode yang dipilih mendukung dan kalibrasinya diperiksa. Kata yang berpengaruh dapat ditampilkan untuk model linear sebagai **kontribusi prediksi**, bukan bukti pasti atau sebab penipuan.

## 8. Spesifikasi web Streamlit: rencana, belum build

**Halaman Periksa SMS:** kolom teks; contoh SMS buatan tim untuk demo; tombol Periksa; validasi input kosong; hasil kategori dengan definisi; indikator pola pesan (misalnya URL atau permintaan OTP) yang jelas dibedakan dari prediksi ML; kontribusi istilah jika model final mendukung; saran tindak lanjut yang sesuai. Jangan membuat URL dalam SMS otomatis dapat diklik. Jangan menyimpan isi SMS pengguna secara default.

**Halaman Tentang Model:** sumber dan batasan dataset, definisi kelas, versi model, tabel kinerja tiga algoritma, metrik per kelas, dan confusion matrix. Tunjukkan bahwa kata/indikator bukan pemeriksaan keamanan URL langsung.

**Fitur tambahan jika waktu cukup:** unggah CSV berisi kolom teks SMS, tampilkan klasifikasi per baris, dan sediakan hasil unduh. Batasi ukuran, cek kolom, dan jangan mempertahankan berkas pengguna setelah proses. Fitur ini bukan syarat utama dan tidak boleh mengorbankan evaluasi model.

**Alur:** input teks → validasi → preprocessing identik dengan training → pipeline TF-IDF dan model tersimpan → label → penjelasan/indikator → hasil di browser. Demo harus menjalankan web secara langsung.

## 9. Studi literatur awal untuk pengajuan

Berikut **lima artikel jurnal kandidat yang dapat ditelusuri**. Ini rencana tabel; sebelum diserahkan, anggota kelompok harus membaca naskah lengkap, memeriksa detail dataset, metrik, hasil, dan perbedaan secara tepat.

| Penulis/tahun | Masalah dan dataset (sejauh abstrak tersedia) | Metode/metrik yang dilaporkan | Hasil/perbedaan dengan rencana ini |
|---|---|---|---|
| [Pramakrisna dkk., 2022, Teknika](https://ejournal.ikado.ac.id/index.php/teknika/article/view/466) | Klasifikasi SMS berbasis web; 1.140 pesan, dua kelas menurut abstrak/metadata | Logistic Regression; aplikasi Flask; detail metrik baca naskah | Rencana ini membandingkan tiga model dan, jika datanya tepat, tiga kelas |
| [Amin dkk., 2024, JTIIK](https://jtiik.ub.ac.id/index.php/jtiik/article/view/8121) | Spam SMS dan email Indonesia | IndoBERT dan MultilingualBERT; laporan akurasi sekitar 98% dan 95% | Menjadi pembanding metode NLP berat; rencana ini memilih pipeline klasik yang ringan dan menganalisis tiga kelas |
| [Yusman, 2025, Khatulistiwa](https://journal.literasikhatulistiwa.org/index.php/kjarti/article/view/253) | 1.143 SMS normal/promosi/penipuan | Multinomial NB, CountVectorizer/TF-IDF, confusion matrix dan metrik klasifikasi; akurasi 93% untuk CountVectorizer menurut abstrak | Dataset/tema berpotensi sama, sehingga perbedaan mesti nyata pada perbandingan tiga algoritma, analisis error, dan web |
| [Asyiah dan Aktavia, 2026, SISKOM-KB](https://jurnal.tau.ac.id/index.php/siskom-kb/article/view/987) | Spam/non-spam; abstrak menyebut 5.572 pesan Indonesia, tetapi asal dan bahasa data perlu diverifikasi | NB, LR, Linear SVM, TF-IDF/CountVectorizer; LR+TF-IDF dilaporkan akurasi 93,89% | Kombinasi algoritma mirip; fokus tiga kelas dan evaluasi penipuan harus menjadi pembeda; cek data asli artikel |
| [Rahmat dan Andhika, 2026, JTS](https://journal.admi.or.id/index.php/JTS/article/view/2948) | Pesan hadiah digital; artikel melaporkan 6.000 pesan, dua kelas | Lima algoritma termasuk XGBoost; akurasi terbaik 97% menurut abstrak | Membantu merumuskan biaya kesalahan dan modus tertentu; dataset artikel belum terkonfirmasi terbuka |

**Catatan integritas:** blog pembagi dataset, Kaggle, GitHub, dan tutorial Medium bukan pengganti lima **artikel jurnal**. Jangan menyalin tabel dari abstrak tanpa memeriksa PDF. Bila salah satu kandidat tidak sesuai setelah pembacaan penuh, ganti dengan jurnal relevan lain.

## 10. Luaran, struktur kerja, dan presentasi

**Source code yang direncanakan:** README (cara instal/jalankan dan sumber dataset), berkas dependensi, notebook/skrip audit dan EDA, skrip training/evaluasi, model pipeline tersimpan, skrip web Streamlit, contoh input aman yang dibuat sendiri. Catat versi dataset, seed, dan label.

**PPT minimum:** judul/anggota; latar belakang; tujuan; tabel lima jurnal; sumber, fitur, label, dan distribusi data; EDA; preprocessing; tiga algoritma dan pembagian data; tabel metrik; alasan model terpilih; arsitektur input-proses-output web; demo; kesimpulan; keterbatasan dan pengembangan; pembagian tugas.

**Video ≤7 menit (rencana waktu):** 0:00–0:35 anggota dan masalah; 0:35–1:25 dataset/literatur; 1:25–2:35 EDA/preprocessing; 2:35–4:10 tiga model/evaluasi/error; 4:10–6:20 demo web hidup dengan SMS contoh normal, promosi, penipuan; 6:20–7:00 kesimpulan, keterbatasan, dan kontribusi anggota. Sesuaikan setelah hasil final.

**Pembagian tugas awal:** Anggota A mengaudit data, menyusun EDA dan definisi label; B membangun tiga pipeline dan evaluasi; C membuat web, integrasi, README, dan demo. Ketiganya meninjau literatur, kesalahan model, PPT, dan harus bisa menjelaskan keseluruhan proyek saat tanya jawab individu.

## 11. Tahapan dan keputusan berikutnya

1. Audit berkas Yudi dan kandidat terbaru yang benar-benar bisa diunduh; putuskan tiga kelas atau biner berdasarkan label nyata. **Ini gerbang sebelum judul dan target final dikunci.**
2. Baca penuh lima jurnal, isi tabel studi literatur final, dan siapkan pengajuan tema.
3. Audit data dan EDA; dokumentasikan pembersihan, distribusi, dan kemungkinan data bocor.
4. Latih tiga model, tuning di training/validasi, evaluasi final di test, analisis error dan over/underfitting.
5. Simpan pipeline terpilih, implementasikan dan uji web Streamlit.
6. Rapikan repositori, PPT, dan video demo langsung ≤7 menit.

**Risiko terbesar saat ini:** sumber kandidat terbaru belum cukup jelas; beberapa penelitian 2025–2026 memakai ulang dataset lama; label biner pada kandidat baru tidak sama dengan target tiga kelas. Keputusan dataset final harus dibuat dari audit berkas, bukan tahun publikasinya.
