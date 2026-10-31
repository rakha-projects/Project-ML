"""
Aplikasi Web Interaktif Deteksi SMS Phishing & Spam Berbahasa Indonesia (Smishing Detector).
Dibuat dengan Streamlit, mengadopsi estetika desain elegan dari example.html:
- Palet Warna: Navy (#263142), Soft Gray (#f1f2f6), Slate Card (#96a2b3), Accent Emerald (#2ecc71), Coral Red (#e74c3c), Amber (#f39c12)
- Tipografi: Plus Jakarta Sans & Poppins
- Tata Letak: Paper-Sheet Card Container dengan Soft Shadow, Rounded Pills & Micro-interactions
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Tambahkan path root Project agar bisa mengimpor src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.preprocessing import clean_text, extract_heuristic_features, detect_language

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="SmishingGuard — Deteksi SMS Phishing & Spam",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INJEKSI CSS KUSTOM (MENGIKUTI ESTETIKA DESAIN EXAMPLE.HTML)
# ==============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800;900&display=swap" rel="stylesheet">

<style>
    /* Styling Dasar Body & Canvas */
    .stApp {
        background-color: #cbd5dc;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #263142;
    }

    /* Sembunyikan elemen default streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Kontainer Lembaran Kertas Putih (Paper-Sheet Container) */
    .block-container {
        max-width: 1140px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        background-color: #ffffff;
        border-radius: 24px;
        margin-top: 24px;
        margin-bottom: 36px;
        box-shadow: 0 25px 60px -15px rgba(30, 41, 59, 0.18);
    }

    /* Header Navigasi Brand */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .brand-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        color: #263142;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .brand-badge {
        font-size: 0.72rem;
        background-color: #263142;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Hero Banner Mini */
    .hero-card {
        background: linear-gradient(135deg, #263142 0%, #1b2432 100%);
        border-radius: 18px;
        padding: 2.2rem 2.5rem;
        color: #ffffff;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px -5px rgba(27, 36, 50, 0.25);
    }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.1rem;
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.85);
        max-width: 680px;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* Kartu Fitur & Statistik */
    .stat-pill {
        background-color: #f1f2f6;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .stat-pill:hover {
        transform: translateY(-2px);
    }
    .stat-val {
        font-size: 1.5rem;
        font-weight: 800;
        color: #263142;
        font-family: 'Poppins', sans-serif;
    }
    .stat-desc {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Kartu Hasil Klasifikasi */
    .result-card-safe {
        background: linear-gradient(135deg, #edfbf2 0%, #dcfae6 100%);
        border: 2px solid #2ecc71;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    .result-card-scam {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #e74c3c;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    .result-card-promo {
        background: linear-gradient(135deg, #fefbeb 0%, #fef3c7 100%);
        border: 2px solid #f39c12;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Tag Lencana Heuristik */
    .heuristic-tag {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .tag-danger {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }
    .tag-warning {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
    }
    .tag-neutral {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
    }
    .tag-success {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }

    /* Tombol Kustom */
    .stButton>button {
        border-radius: 9999px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(38, 49, 66, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. FUNGSI PEMUATAN MODEL & ARTEFAK DENGAN CACHING
# ==============================================================================
@st.cache_resource
def load_ml_assets():
    models_dir = os.path.join(BASE_DIR, "models")
    
    # 1. Model Bahasa Indonesia
    vec_id = joblib.load(os.path.join(models_dir, "tfidf_vectorizer_id.joblib"))
    model_id = joblib.load(os.path.join(models_dir, "best_model_id.joblib"))
    
    # 2. Model Bahasa Inggris
    vec_en = joblib.load(os.path.join(models_dir, "tfidf_vectorizer_en.joblib"))
    model_en = joblib.load(os.path.join(models_dir, "best_model_en.joblib"))
    
    # 3. Model Pembanding (Untuk Halaman Evaluasi)
    nb_id = joblib.load(os.path.join(models_dir, "multinomial_naive_bayes_id.joblib"))
    svm_id = joblib.load(os.path.join(models_dir, "linear_svm_id.joblib"))

    # 4. Tabel Perbandingan Metrik
    comp_path = os.path.join(models_dir, "model_comparison_id.json")
    with open(comp_path, "r", encoding="utf-8") as f:
        comp_data = json.load(f)

    return {
        "vec_id": vec_id,
        "model_id": model_id,
        "vec_en": vec_en,
        "model_en": model_en,
        "nb_id": nb_id,
        "svm_id": svm_id,
        "comp_data": comp_data
    }

try:
    assets = load_ml_assets()
except Exception as e:
    st.error(f"Gagal memuat artefak model dari folder Project/models: {e}")
    st.stop()


# ==============================================================================
# 4. NAVBAR & HEADER BRAND (MENGIKUTI NAVBAR DI EXAMPLE.HTML)
# ==============================================================================
st.markdown("""
<div class="brand-header">
    <div class="brand-title">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#263142" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        SMISHING<span style="color:#e74c3c;">GUARD</span>
        <span class="brand-badge">ML 2026</span>
    </div>
    <div style="font-size: 0.82rem; color: #64748b; font-weight: 500;">
        Sistem Klasifikasi & Proteksi Pesan Siber Dwibahasa (ID / EN)
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 5. SIDEBAR: PENGATURAN & INFORMASI AKADEMIK
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi Sistem")
    
    mode_bahasa = st.selectbox(
        "Mode Deteksi Bahasa:",
        ["Deteksi Otomatis (Auto-Detect)", "Paksa Bahasa Indonesia", "Force English (Bahasa Inggris)"],
        index=0,
        help="Sistem secara cerdas memilih pipeline normalisasi leksikal dan model terbaik sesuai bahasa pesan."
    )

    st.markdown("---")
    st.markdown("### 🏆 Informasi Proyek")
    st.markdown("""
    - **Topik**: Text Classification (Smishing)
    - **Dataset**: Yudi Wibisono & Corpus En (14 Kolom Seragam)
    - **Algoritma Terpilih**: **Logistic Regression (L2)**
    - **Akurasi Model**: **97.37%** (Test Set)
    - **F1-Score Macro**: **96.68%**
    - **Recall Penipuan**: **95.45%**
    """)

    st.markdown("---")
    st.caption("Dikembangkan untuk Memenuhi Syarat Tugas Akhir Mata Kuliah Pembelajaran Mesin (Semester 5).")


# ==============================================================================
# 6. TAB NAVIGASI UTAMA
# ==============================================================================
tab_scanner, tab_batch, tab_eval, tab_anatomy = st.tabs([
    "🔍 Pemindai SMS Real-Time",
    "📁 Pemeriksaan Massal (Batch CSV)",
    "📊 Dashboard Evaluasi & Model",
    "🛡️ Anatomi Modus Penipuan"
])


# ==============================================================================
# 7. TAB 1: PEMINDAI SMS REAL-TIME (SINGLE SCANNER)
# ==============================================================================
with tab_scanner:
    # Hero Card Section
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Periksa Keamanan SMS Anda Seketika</div>
        <p class="hero-subtitle">
            Lindungi diri dari sindikat pinjaman online ilegal, penipuan undian berhadiah palsu, dan tautan phishing malware menggunakan model Machine Learning terkalibrasi tinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3 Statistik Cepat (Mengikuti 3 Stat Badges di example.html)
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
        <div class="stat-pill">
            <div class="stat-val">97.37%</div>
            <div class="stat-desc">Akurasi Deteksi</div>
        </div>
        <div class="stat-pill">
            <div class="stat-val">95.45%</div>
            <div class="stat-desc">Recall Penipuan</div>
        </div>
        <div class="stat-pill">
            <div class="stat-val">&lt; 50 ms</div>
            <div class="stat-desc">Kecepatan Inferensi</div>
        </div>
        <div class="stat-pill">
            <div class="stat-val">0% Leakage</div>
            <div class="stat-desc">Privasi Terjaga</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol Preset Contoh Pesan Cepat (One-Click Examples)
    st.markdown("##### 💡 Coba Contoh Pesan Cepat (Quick Demo):")
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    
    preset_text = ""
    if col_ex1.button("🟢 Contoh Normal (ID)", use_container_width=True):
        st.session_state["sms_input"] = "Besok kuliah jam 8 pagi di lab komputer jangan lupa bawa laptop dan charger ya bro."
    if col_ex2.button("🟡 Contoh Promosi (ID)", use_container_width=True):
        st.session_state["sms_input"] = "[PROMO] Beli paket Flash mulai 1GB di MY TELKOMSEL APP dpt EXTRA kuota 2GB 4G LTE. Buruan cek di tsel.me/mytsel1 S&K *363#"
    if col_ex3.button("🔴 Contoh Penipuan (ID)", use_container_width=True):
        st.session_state["sms_input"] = "Selamat No anda m-dptkan Cek Tunai 100jt dr Shopee. PIN pemenang: 254F77 Hub WA: 082134976289 atau klik http://shopee-klaim.xyz/dana Segera lapor rek anda!"
    if col_ex4.button("🇬🇧 Contoh Scam (EN)", use_container_width=True):
        st.session_state["sms_input"] = "URGENT! You have won a 1000 cash prize or 1 week holiday to Hawaii! Call 09061701461 now to claim your prize. Terms apply."

    # Input Area Teks SMS
    current_input = st.session_state.get("sms_input", "")
    sms_text = st.text_area(
        "Tempelkan isi teks SMS yang ingin diperiksa:",
        value=current_input,
        height=110,
        placeholder="Ketik atau tempel isi pesan SMS di sini...",
        key="sms_text_area"
    )

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        btn_check = st.button("🛡️ Periksa SMS Sekarang", type="primary", use_container_width=True)
    with col_info:
        if sms_text:
            st.caption(f"Panjang teks: **{len(sms_text)}** karakter | **{len(sms_text.split())}** kata")

    # Logika Pemrosesan & Prediksi
    if btn_check:
        if not sms_text.strip():
            st.warning("⚠️ Silakan masukkan teks SMS terlebih dahulu sebelum menekan tombol periksa.")
        else:
            # 1. Deteksi Bahasa
            if "Indonesia" in mode_bahasa:
                lang_code = "id"
                lang_display = "Bahasa Indonesia (Dipaksa Manual)"
            elif "English" in mode_bahasa:
                lang_code = "en"
                lang_display = "English (Forced Manual)"
            else:
                det = detect_language(sms_text)
                lang_code = det["language"]
                lang_display = f"{det['language_name']} (Keyakinan: {det['confidence']*100:.0f}%)"

            # 2. Pembersihan & Ekstraksi Heuristik
            cleaned = clean_text(sms_text, lang=lang_code)
            heur = extract_heuristic_features(sms_text, lang=lang_code)

            # 3. Inferensi Model
            if lang_code == "en":
                vec = assets["vec_en"]
                model = assets["model_en"]
            else:
                vec = assets["vec_id"]
                model = assets["model_id"]

            vec_input = vec.transform([cleaned])
            pred_class = model.predict(vec_input)[0]
            pred_probs = model.predict_proba(vec_input)[0]

            class_labels = ["Normal", "Penipuan", "Promosi"]
            pred_label = class_labels[pred_class]
            prob_safe = pred_probs[0] * 100
            prob_scam = pred_probs[1] * 100
            prob_promo = pred_probs[2] * 100

            # 4. Tampilkan Kartu Hasil Klasifikasi
            st.markdown("---")
            st.markdown(f"#### 📊 Hasil Analisis Pesan | Bahasa Terdeteksi: `{lang_display}`")

            if pred_label == "Penipuan":
                st.markdown(f"""
                <div class="result-card-scam">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="color:#991b1b; margin:0; font-family:'Poppins',sans-serif; font-weight:800;">
                            🚨 INDIKASI PENIPUAN (PHISHING / SMISHING)
                        </h3>
                        <span style="background-color:#991b1b; color:#fff; padding:6px 14px; border-radius:9999px; font-weight:700; font-size:0.85rem;">
                            Tingkat Bahaya: TINGGI
                        </span>
                    </div>
                    <p style="color:#7f1d1d; margin-top:0.6rem; font-size:0.92rem; line-height:1.5;">
                        Model mendeteksi pola manipulasi rekayasa sosial (*social engineering*), pancingan dana/hadiah, atau tautan berbahaya. 
                        Tingkat keyakinan model: <strong>{prob_scam:.2f}%</strong>.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            elif pred_label == "Promosi":
                st.markdown(f"""
                <div class="result-card-promo">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="color:#92400e; margin:0; font-family:'Poppins',sans-serif; font-weight:800;">
                            📢 SMS PROMOSI / IKLAN RESMI
                        </h3>
                        <span style="background-color:#f59e0b; color:#fff; padding:6px 14px; border-radius:9999px; font-weight:700; font-size:0.85rem;">
                            Tingkat Risiko: RENDAH
                        </span>
                    </div>
                    <p style="color:#78350f; margin-top:0.6rem; font-size:0.92rem; line-height:1.5;">
                        Pesan ini diidentifikasi sebagai penawaran produk, paket internet, atau buletin resmi dari operator telekomunikasi/merchant terdaftar.
                        Tingkat keyakinan model: <strong>{prob_promo:.2f}%</strong>.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="result-card-safe">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="color:#166534; margin:0; font-family:'Poppins',sans-serif; font-weight:800;">
                            ✅ SMS NORMAL (KOMUNIKASI WAJAR)
                        </h3>
                        <span style="background-color:#16a34a; color:#fff; padding:6px 14px; border-radius:9999px; font-weight:700; font-size:0.85rem;">
                            Status: AMAN
                        </span>
                    </div>
                    <p style="color:#14532d; margin-top:0.6rem; font-size:0.92rem; line-height:1.5;">
                        Pesan ini menunjukkan karakteristik komunikasi santai, percakapan sehari-hari, atau pesan kedinasan yang wajar tanpa indikasi ancaman siber.
                        Tingkat keyakinan model: <strong>{prob_safe:.2f}%</strong>.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # 5. Bar Probabilitas Kelas
            st.markdown("##### 📈 Distribusi Probabilitas Keyakinan Model:")
            col_p1, col_p2, col_p3 = st.columns(3)
            col_p1.metric("Peluang Normal", f"{prob_safe:.2f}%")
            col_p2.metric("Peluang Penipuan", f"{prob_scam:.2f}%")
            col_p3.metric("Peluang Promosi", f"{prob_promo:.2f}%")

            # Progress bar visual
            st.progress(max(0.0, min(1.0, prob_scam / 100.0)), text=f"Skor Ancaman Penipuan: {prob_scam:.1f}%")

            # 6. Analisis Indikator Heuristik Keamanan
            st.markdown("##### 🔬 Faktor Risiko Heuristik Terdeteksi:")
            tag_html = ""
            if heur["has_url"]:
                tag_html += f'<span class="heuristic-tag tag-danger">🔗 Tautan Terdeteksi ({len(heur["urls_detected"])})</span>'
            else:
                tag_html += '<span class="heuristic-tag tag-neutral">Bebas Tautan</span>'

            if heur["has_phone"]:
                tag_html += f'<span class="heuristic-tag tag-danger">📞 Nomor Telepon/WA Pribadi ({len(heur["phones_detected"])})</span>'
            else:
                tag_html += '<span class="heuristic-tag tag-neutral">Tanpa Nomor Pribadi</span>'

            if heur["has_nominal"]:
                tag_html += f'<span class="heuristic-tag tag-warning">💰 Mencantumkan Nominal Uang</span>'

            if heur["has_shortcode"]:
                tag_html += f'<span class="heuristic-tag tag-success">🔢 Kode USSD Resmi Operator</span>'

            if heur["urgency_keywords"]:
                tag_html += f'<span class="heuristic-tag tag-danger">⏰ Kata Urgensi: {", ".join(heur["urgency_keywords"])}</span>'

            if heur["financial_keywords"]:
                tag_html += f'<span class="heuristic-tag tag-warning">💳 Istilah Finansial: {", ".join(heur["financial_keywords"])}</span>'

            st.markdown(tag_html, unsafe_allow_html=True)

            # 7. Teks Hasil Normalisasi (Explainability)
            with st.expander("🛠️ Lihat Teks Hasil Preprocessing & Masking Token"):
                st.code(cleaned, language="text")
                st.caption("Pemberitahuan: URL diubah menjadi `[url]`, kontak menjadi `[nomor]`, dan nominal uang menjadi `[nominal]` untuk standarisasi inferensi.")

            # 8. Rekomendasi Tindakan Keamanan
            st.markdown("##### 🛡️ Rekomendasi Tindakan Pengguna:")
            if pred_label == "Penipuan":
                st.error("""
                1. **JANGAN PERNAH** mengklik tautan/link yang ada di dalam pesan tersebut.
                2. **JANGAN** menghubungi nomor telepon atau nomor WhatsApp yang dicantumkan.
                3. **JANGAN** membagikan kode OTP, password, atau nomor rekening bank Anda kepada siapa pun.
                4. Laporkan pengirim nomor ke layanan pengaduan resmi: **aduankonten.id (Kominfo)** atau ke CS bank resmi Anda.
                """)
            elif pred_label == "Promosi":
                st.info("""
                1. Pesan ini merupakan penawaran promo atau kuota dari operator resmi.
                2. Jika Anda tertarik, pastikan bertransaksi hanya melalui kode dial resmi (seperti `*363#`) atau aplikasi resmi operator (MyTelkomsel, myIM3, bima+).
                """)
            else:
                st.success("""
                1. Pesan ini aman untuk dibaca dan direspon secara normal.
                2. Tetap waspada jika di kemudian hari pengirim meminta data pribadi atau transfer uang tak terduga.
                """)


# ==============================================================================
# 8. TAB 2: PEMERIKSAAN MASSAL (BATCH CSV SCANNER)
# ==============================================================================
with tab_batch:
    st.markdown("### 📁 Pemeriksaan SMS Massal via File CSV")
    st.markdown("Unggah file CSV yang memuat daftar SMS untuk dianalisis secara otomatis oleh model Machine Learning.")

    uploaded_file = st.file_uploader("Pilih file CSV:", type=["csv"])

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.write(f"Total baris ditemukan: **{len(df_upload)} baris**")

            # Pilih Kolom Teks
            text_columns = df_upload.select_dtypes(include=["object"]).columns.tolist()
            if not text_columns:
                st.error("Tidak ditemukan kolom teks dalam file CSV.")
            else:
                selected_col = st.selectbox("Pilih kolom yang berisi teks SMS:", text_columns)

                if st.button("🚀 Mulai Pemindaian Massal", type="primary"):
                    with st.spinner("Sedang memproses seluruh pesan..."):
                        preds = []
                        confidences = []
                        risk_scores = []
                        langs = []

                        vec_id = assets["vec_id"]
                        model_id = assets["model_id"]
                        class_labels = ["Normal", "Penipuan", "Promosi"]

                        for raw_t in df_upload[selected_col].astype(str):
                            det = detect_language(raw_t)
                            c_text = clean_text(raw_t, lang=det["language"])
                            heur = extract_heuristic_features(raw_t, lang=det["language"])

                            v = vec_id.transform([c_text])
                            p = model_id.predict(v)[0]
                            prob = model_id.predict_proba(v)[0][p] * 100

                            preds.append(class_labels[p])
                            confidences.append(round(prob, 2))
                            risk_scores.append(heur["heuristic_risk_score"])
                            langs.append(det["language_name"])

                        df_result = df_upload.copy()
                        df_result["Prediksi_Kategori"] = preds
                        df_result["Keyakinan_Model_%"] = confidences
                        df_result["Skor_Risiko_Heuristik"] = risk_scores
                        df_result["Bahasa"] = langs

                        st.success("✅ Pemindaian massal selesai!")

                        # Ringkasan Distribusi
                        c1, c2, c3 = st.columns(3)
                        counts = df_result["Prediksi_Kategori"].value_counts()
                        c1.metric("Total Normal (Aman)", counts.get("Normal", 0))
                        c2.metric("Total Penipuan (Waspada)", counts.get("Penipuan", 0))
                        c3.metric("Total Promosi", counts.get("Promosi", 0))

                        # Tampilkan Dataframe Interaktif
                        st.dataframe(df_result, use_container_width=True)

                        # Tombol Unduh Hasil
                        csv_download = df_result.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="📥 Unduh Hasil Klasifikasi (CSV)",
                            data=csv_download,
                            file_name="Hasil_Deteksi_SMS_Batch.csv",
                            mime="text/csv",
                            type="secondary"
                        )
        except Exception as err:
            st.error(f"Gagal memproses file CSV: {err}")


# ==============================================================================
# 9. TAB 3: DASHBOARD EVALUASI & TRANSPARANSI MODEL (ACADEMIC BENCHMARK)
# ==============================================================================
with tab_eval:
    st.markdown("### 📊 Evaluasi Model & Transparansi Akademik (M15)")
    st.markdown("Ringkasan ilmiah hasil eksperimen 3 model Machine Learning sesuai dengan rubrik tugas akhir:")

    # 1. Tabel Perbandingan Metrik
    st.markdown("##### 1. Tabel Perbandingan Kinerja 3 Algoritma (Test Set N=228):")
    comp_df = pd.DataFrame(assets["comp_data"])
    show_cols = {
        "model_name": "Algoritma",
        "accuracy": "Akurasi",
        "f1_macro": "Macro F1-Score",
        "recall_penipuan": "Recall Penipuan",
        "recall_normal": "Recall Normal",
        "cv_f1_macro_mean": "5-Fold CV Macro F1"
    }
    st.dataframe(comp_df[list(show_cols.keys())].rename(columns=show_cols), use_container_width=True)

    # 2. Grafik Confusion Matrix & Feature Importance
    c_img1, c_img2 = st.columns(2)
    with c_img1:
        st.markdown("##### 2. Confusion Matrix Heatmap:")
        cm_file = os.path.join(RESULTS_DIR, "confusion_matrices.png")
        if os.path.exists(cm_file):
            st.image(cm_file, caption="Confusion Matrix 3 Model (Naive Bayes, Logistic Regression, Linear SVM)", use_container_width=True)
    with c_img2:
        st.markdown("##### 3. Fitur Kata Penentu (Feature Importance):")
        fi_file = os.path.join(RESULTS_DIR, "feature_importance.png")
        if os.path.exists(fi_file):
            st.image(fi_file, caption="Bobot Koefisien Leksikal Penentu Kategori", use_container_width=True)

    # 3. Analisis Ilmiah Generalisasi
    st.markdown("##### 4. Analisis Overfitting & Justifikasi Ilmiah:")
    st.info("""
    - **Pemeriksaan Overfitting**: Logistic Regression menghasilkan Akurasi Latih **99.45%** dan Akurasi Uji **97.37%** (Gap sangat kecil yaitu **+2.08%**). Terbukti model memiliki generalisasi yang **Optimal (Good Fit)** tanpa *data leakage*.
    - **Alasan Pemilihan Logistic Regression**: Selain akurasi dan Macro-F1 tertinggi (96.68%), model ini menghasilkan estimasi probabilitas terkalibrasi (`predict_proba()`) dan memiliki **Recall Penipuan 95.45%**, sehingga meminimalkan risiko bahaya pesan penipuan yang lolos.
    """)


# ==============================================================================
# 10. TAB 4: PANDUAN EDUKASI & ANATOMI MODUS SMISHING
# ==============================================================================
with tab_anatomy:
    st.markdown("### 🛡️ Panduan Edukasi: Mengenali Modus Smishing di Indonesia")
    st.markdown("Pelajari pola taktik rekayasa sosial yang kerap digunakan oleh sindikat penipuan SMS:")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:1.25rem; margin-bottom:1rem;">
            <h4 style="color:#b91c1c; margin-top:0;">1. Modus APK Kurir & Undangan Palsu</h4>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                Pelaku mengirim pesan berpura-pura menjadi kurir pengantar paket (J&T, SiCepat) atau undangan pernikahan, lalu menyuruh korban mengunduh file berekstensi <code>.APK</code>. File ini adalah malware <em>SMS-Sniffer</em> yang mencuri kode OTP perbankan korban.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:1.25rem;">
            <h4 style="color:#b91c1c; margin-top:0;">2. Modus Undian Pemenang Shopee / Bank</h4>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                Pelaku mengabarkan nomor korban memenangkan cek tunai ratusan juta rupiah lengkap dengan nomor PIN pemenang palsu dan nomor WhatsApp. Korban kemudian diminta membayar biaya administrasi atau mentransfer sejumlah uang.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:1.25rem; margin-bottom:1rem;">
            <h4 style="color:#b91c1c; margin-top:0;">3. Modus Pinjaman Online (Pinjol) Ilegal</h4>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                Penawaran pinjaman dana tunai cepat tanpa jaminan hanya dengan syarat KTP, bunga rendah (0.99%), dan cair dalam hitungan jam. Pelaku mencantumkan nomor WhatsApp pribadi atau link formulir pencurian data identitas.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:1.25rem;">
            <h4 style="color:#b91c1c; margin-top:0;">4. Modus Notifikasi Rekening Diblokir</h4>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                Pesan darurat yang mengancam bahwa kartu ATM atau rekening bank korban akan diblokir karena ada aktivitas mencurigakan. Korban diarahkan ke situs phishing palsu untuk memasukkan user ID dan PIN internet banking.
            </p>
        </div>
        """, unsafe_allow_html=True)

