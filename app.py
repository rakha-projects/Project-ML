"""SmishingGuard: a real model-backed Streamlit application."""
from __future__ import annotations

import hashlib
import html
import io
import time

import pandas as pd
import streamlit as st

from src.app_data import ROOT, load_resources, parse_csv
from src.inference import LABELS, MAX_SMS_CHARS, analyze_batch, analyze_sms, safe_csv_bytes
from src.visuals import png_markup

st.set_page_config(page_title='SmishingGuard | Periksa SMS', layout='wide',
                   initial_sidebar_state='collapsed')
st.html(f"<style>{(ROOT / 'assets/app.css').read_text(encoding='utf-8-sig')}</style>")

LANGUAGES = {'Otomatis': 'auto', 'Bahasa Indonesia': 'id', 'English': 'en'}
LANG_NAMES = {'id': 'Bahasa Indonesia', 'en': 'English'}
COLORS = {'Normal': '#236447', 'Penipuan': '#b13b3b', 'Promosi': '#a77021'}
EXAMPLES = {
    'Indonesia': {
        'Normal': 'Besok kuliah jam delapan pagi di laboratorium. Jangan lupa bawa laptop ya.',
        'Promosi': 'Paket Flash Spesial! Nikmati kuota 25GB berlaku 30 hari hanya Rp 50.000. Aktifkan di *363*88#. Syarat dan ketentuan berlaku.',
        'Penipuan': 'Selamat! Nomor Anda terpilih mendapat hadiah cek tunai Rp 100 juta. Segera klaim hadiah, hubungi WA 081234567890 dan kirim data rekening Anda.',
    },
    'English': {
        'Normal': 'Hey, are we still meeting at the library tomorrow morning? Please bring your laptop.',
        'Promosi': 'Special offer! Get 150 free texts and 750 minutes for only 5 pounds per week. Reply YES to subscribe. Terms apply.',
        'Penipuan': 'URGENT! You have won a 1000 cash prize! Call 09061701461 to claim your reward immediately. Send your bank account details now.',
    },
}
SHIELD = '<svg viewBox="0 0 64 72" fill="none" aria-hidden="true"><path d="M32 4 57 14v20c0 16-11 27-25 34C18 61 7 50 7 34V14L32 4Z" fill="currentColor" fill-opacity=".08" stroke="currentColor" stroke-width="2.5"/><path d="m21 35 8 8 16-19" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m4 10 4 4 8-8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>'


@st.cache_resource
def resources():
    return load_resources()


try:
    PIPELINES, EVALUATION = resources()
except (OSError, ValueError, KeyError, AttributeError, ImportError) as error:
    st.error(f'Aplikasi belum dapat memuat model. {error}')
    st.code('python -m pip install -r requirements.txt\npython -m src.train\npython -m src.evaluate')
    st.stop()

INDO = EVALUATION['indonesian']
SELECTED = next(model for model in INDO['models'] if model['model_name'] == INDO['selected_model'])


def percent(value):
    return f'{value * 100:.2f}%'


def intro(title, description):
    st.html(f'<div class="section-intro"><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p></div>')


def reset_sms():
    st.session_state.sms_text = ''
    st.session_state.pop('single_result', None)
    st.session_state.pop('single_error', None)


def predict_single():
    text = st.session_state.sms_text
    mode = LANGUAGES[st.session_state.sms_language]
    st.session_state.pop('single_error', None)
    st.session_state.pop('single_result', None)
    try:
        started = time.perf_counter()
        result = analyze_sms(text, mode, PIPELINES)
        result['elapsed_ms'] = (time.perf_counter() - started) * 1000
        st.session_state.single_result = {'text': text, 'mode': mode, 'result': result}
    except ValueError as error:
        st.session_state.single_error = str(error)


def set_example(category):
    collection = st.session_state.example_language
    st.session_state.sms_text = EXAMPLES[collection][category]
    st.session_state.sms_language = 'Bahasa Indonesia' if collection == 'Indonesia' else 'English'
    predict_single()


def show_result(result):
    label = result['label']
    confidence = result['probabilities'][label] * 100
    st.html(f'<div class="result-card {label.lower()}"><small>Prediksi kategori pesan</small>'
            f'<div class="result-label" style="color:{COLORS[label]}">{label}</div>'
            f'<small>{LANG_NAMES[result["language"]]} · Keyakinan model {confidence:.1f}%</small></div>')
    score = result['fraud_score']
    circumference = 2 * 3.14159265 * 44
    st.html(f'''<div class="score-row"><svg viewBox="0 0 110 110" role="img" aria-label="Skor kelas Penipuan {score:.1f} persen">
    <circle cx="55" cy="55" r="44" fill="none" stroke="#edf1ee" stroke-width="7"/>
    <circle cx="55" cy="55" r="44" fill="none" stroke="#b13b3b" stroke-width="7" stroke-linecap="round"
    stroke-dasharray="{circumference * score / 100:.2f} {circumference:.2f}" transform="rotate(-90 55 55)"/>
    <text x="55" y="58" text-anchor="middle" fill="#162d25" font-size="21" font-weight="650">{score:.1f}%</text>
    <text x="55" y="75" text-anchor="middle" fill="#60736b" font-size="10">PENIPUAN</text></svg>
    <div><strong>Skor kelas Penipuan</strong><p>Keluaran model dari pola teks. Skor ini tidak memverifikasi keamanan pesan atau pengirim.</p></div></div>''')
    for name in LABELS.values():
        value = result['probabilities'][name] * 100
        st.html(f'<div class="probability"><div class="labels"><span>{name}</span><strong>{value:.1f}%</strong></div>'
                f'<div class="track"><div class="fill" style="width:{value:.2f}%;background:{COLORS[name]}"></div></div></div>')
    advice = {
        'Penipuan': 'Tunda merespons. Jangan bagikan OTP, PIN, atau data rekening. Konfirmasi permintaan melalui kanal resmi yang Anda cari sendiri.',
        'Promosi': 'Pesan menyerupai penawaran produk. Periksa pengirim, harga, dan syaratnya melalui aplikasi atau kanal resmi sebelum menindaklanjuti.',
        'Normal': 'Pesan menyerupai percakapan biasa. Tetap konfirmasi jika ada permintaan uang, data pribadi, atau pemasangan aplikasi.',
    }
    st.html(f'<div class="guidance"><strong>Langkah berikutnya</strong><br>{advice[label]}</div>')
    if result['no_known_terms']:
        st.warning('Kosakata pesan tidak dikenali model. Prediksi ini tidak cukup untuk mengambil keputusan; periksa pesan secara manual.')
    elif confidence < 60:
        st.warning('Model belum yakin pada satu kategori. Periksa konteks pesan dan identitas pengirim secara manual.')
    if result['language_ambiguous']:
        st.info('Bahasa pesan sulit dipastikan dari kata yang tersedia. Pilih bahasa secara manual untuk membandingkan hasil.')
    if result['language'] == 'en':
        st.caption('Model Inggris bersifat eksploratif. Asal korpus masih perlu diverifikasi independen.')
    st.caption(f"Model: {INDO['selected_model'] if result['language'] == 'id' else EVALUATION['english']['model_name']} · Inferensi {result['elapsed_ms']:.0f} ms")


def show_explanation(result):
    st.divider()
    left, right = st.columns([1, 1], gap='large')
    with left:
        st.subheader('Pola yang ditemukan')
        st.caption('Indikator berbasis aturan; dihitung terpisah dari probabilitas model.')
        heuristics = result['heuristics']
        cols = st.columns(2)
        patterns = [('Tautan web', 'has_url', 'urls_detected'), ('Nomor kontak', 'has_phone', 'phones_detected'),
                    ('Nominal uang', 'has_nominal', 'nominals_detected'), ('Kode layanan', 'has_shortcode', 'codes_detected')]
        for index, (title, flag, values) in enumerate(patterns):
            with cols[index % 2]:
                found = heuristics[flag]
                st.html(f'<div class="indicator {"found" if found else ""}"><strong>{title}</strong>'
                        f'<small>{"Terdeteksi" if found else "Tidak terdeteksi"}</small></div>')
        with st.expander('Lihat rincian indikator'):
            for title, flag, values in patterns:
                if heuristics[flag]:
                    st.write(title)
                    st.code('\n'.join(heuristics[values]), language=None, wrap_lines=True)
            keywords = heuristics['urgency_keywords'] + heuristics['financial_keywords']
            st.write('Kata pemicu: ' + (', '.join(keywords) if keywords else 'Tidak ditemukan'))
            st.caption(f"Skor aturan: {heuristics['heuristic_risk_score']}/100. Penjumlahan bobot aturan, bukan probabilitas dan tidak mengubah label model.")
    with right:
        st.subheader('Mengapa model memilih kategori ini?')
        st.caption('Kata atau frasa dengan kontribusi positif pada prediksi saat ini.')
        if result['contributions']:
            st.html(''.join(f'<span class="term">{html.escape(term["term"])}</span>' for term in result['contributions']))
            if result['contributions_approximate']:
                st.caption('Perkiraan dari rata-rata bobot model SVM terkalibrasi; bukan penjelasan kausal atau probabilitas per kata.')
        else:
            st.caption('Tidak ada kontribusi kata positif yang dapat ditampilkan untuk pesan ini.')
        with st.expander('Lihat teks setelah preprocessing'):
            st.code(result['cleaned_text'], language=None, wrap_lines=True)
            st.caption('Huruf kecil, penyamaran entitas, pembersihan karakter, lalu normalisasi singkatan. Proses yang sama digunakan saat pelatihan.')


def scanner():
    intro('Kenali pesan sebelum merespons.', 'Tempel isi SMS atau coba contoh. Model membaca pola teks dalam tiga kategori.')
    left, right = st.columns([1.15, 1], gap='large')
    with left, st.container(key='input_panel'):
        st.html('<div class="panel-heading"><h3>Isi pesan SMS</h3><span class="tag">Maks. 2.000 karakter</span></div>')
        st.selectbox('Bahasa analisis', list(LANGUAGES), key='sms_language',
                     help='Deteksi otomatis memakai aturan kata. Pilih manual untuk pesan pendek atau campuran.')
        text = st.text_area('Teks SMS', key='sms_text', height=180, max_chars=MAX_SMS_CHARS,
                            placeholder='Tempel pesan yang ingin diperiksa di sini…', label_visibility='collapsed')
        st.caption(f'{len(text):,} / {MAX_SMS_CHARS:,} karakter · {len(text.split())} kata')
        a, b = st.columns([1.4, 1])
        a.button('Periksa pesan', type='primary', on_click=predict_single, width='stretch')
        b.button('Kosongkan', on_click=reset_sms, width='stretch')
        if st.session_state.get('single_error'):
            st.error(st.session_state.single_error)
        st.divider()
        st.selectbox('Coba contoh pesan', list(EXAMPLES), key='example_language')
        presets = st.columns(3)
        for column, label in zip(presets, LABELS.values()):
            column.button(label, key=f'preset_{label}', on_click=set_example, args=(label,), width='stretch')
        st.caption('Contoh ilustratif untuk mencoba fitur; prediksi tetap dihitung oleh model.')
    saved = st.session_state.get('single_result')
    current = saved and saved['text'] == text and saved['mode'] == LANGUAGES[st.session_state.sms_language]
    with right, st.container(key='result_panel'):
        st.html('<div class="panel-heading"><h3>Hasil analisis</h3><span class="tag">Model ML terlatih</span></div>')
        if current:
            show_result(saved['result'])
        else:
            st.html(f'<div class="empty-result" style="color:#236447">{SHIELD}<h3>{"Pesan telah berubah" if saved else "Siap membaca pola pesan"}</h3>'
                    '<p>Tekan Periksa pesan untuk melihat kategori, skor model, dan penjelasan kata yang berpengaruh.</p>'
                    '<div class="empty-categories"><span>Normal</span><span>Penipuan</span><span>Promosi</span></div></div>')
    st.caption('Privasi: teks diproses di memori sesi dan tidak ditulis ke disk oleh aplikasi. Tautan dalam SMS tidak dibuka.')
    if current:
        show_explanation(saved['result'])


def batch():
    intro('Periksa banyak pesan sekaligus.', 'Unggah CSV, pilih kolom teks, lalu unduh hasil lengkap dengan status setiap baris.')
    left, right = st.columns([1.8, 1], gap='large')
    with left, st.container(key='batch_panel'):
        st.subheader('Unggah daftar SMS')
        upload = st.file_uploader('Berkas CSV', type=['csv'], help='Maksimal 2 MB, 1.000 baris, dengan header kolom.')
        opts = st.columns(3)
        language = opts[0].selectbox('Bahasa batch', list(LANGUAGES), key='batch_language')
        separator = opts[1].selectbox('Pemisah CSV', ['Otomatis', ',', ';', '\t'],
                                     format_func=lambda value: {'\t': 'Tab', ',': 'Koma (,)', ';': 'Titik koma (;)'}.get(value, value))
        encoding = opts[2].selectbox('Encoding', ['Otomatis', 'utf-8-sig', 'cp1252'],
                                    format_func=lambda value: {'utf-8-sig': 'UTF-8', 'cp1252': 'Windows-1252'}.get(value, value))
    with right:
        st.subheader('Mulai dari contoh')
        st.write('Satu baris untuk satu pesan. Kolom tambahan seperti ID tetap ikut di hasil unduhan.')
        st.download_button('Unduh CSV contoh', data=(ROOT / 'laporan/contoh_sms.csv').read_bytes(),
                           file_name='contoh_sms.csv', mime='text/csv', width='stretch')
        st.caption('Maks. 2 MB · 1.000 baris · 2.000 karakter/pesan. Baris kosong atau terlalu panjang ditandai tanpa menghentikan baris lainnya.')
    if upload is None:
        return
    try:
        data = upload.getvalue()
        frame = parse_csv(data, separator, encoding)
    except ValueError as error:
        st.error(str(error))
        return
    candidates = [col for col in frame.columns if str(col).lower().strip() in ('text', 'sms', 'teks', 'message', 'pesan')]
    column = st.selectbox('Kolom berisi teks SMS', list(frame.columns),
                          index=list(frame.columns).index(candidates[0]) if candidates else 0)
    st.caption(f'{len(frame):,} baris · {len(frame.columns)} kolom · {len(data)/1024:.1f} KB')
    with st.expander('Pratinjau data masukan', expanded=True):
        st.dataframe(frame.head(5), hide_index=True, width='stretch')
    signature = (hashlib.sha256(data).hexdigest(), column, language, separator, encoding)
    if st.button('Proses semua pesan', type='primary'):
        with st.spinner(f'Menganalisis {len(frame):,} pesan…'):
            start = time.perf_counter()
            output = analyze_batch(frame, column, LANGUAGES[language], PIPELINES)
            st.session_state.batch_result = {'signature': signature, 'output': output,
                                             'seconds': time.perf_counter() - start}
    saved = st.session_state.get('batch_result')
    if not saved or saved['signature'] != signature:
        return
    output = saved['output']
    valid = output['Prediksi_Kategori'].isin(LABELS.values())
    st.divider()
    st.subheader('Ringkasan hasil batch')
    a, b, c, d = st.columns(4)
    a.metric('Berhasil dianalisis', f'{int(valid.sum()):,}')
    b.metric('Perlu tinjauan', f"{int((output['Status'] == 'Perlu tinjauan').sum()):,}")
    c.metric('Baris tidak valid', f'{int((~valid).sum()):,}')
    d.metric('Waktu proses', f"{saved['seconds']:.2f} dtk")
    chart_col, count_col = st.columns([1.5, 1])
    counts = output.loc[valid, 'Prediksi_Kategori'].value_counts().reindex(list(LABELS.values()), fill_value=0)
    with chart_col:
        st.bar_chart(counts.rename('Jumlah pesan'), color='#236447', horizontal=True, height=220)
    with count_col:
        st.write('Distribusi kategori')
        for name, count in counts.items():
            st.write(f'{name}: **{count} pesan**')
        st.caption('Kategori Normal maupun Promosi tidak memverifikasi pengirim atau keamanan tautan.')
    category = st.selectbox('Filter tabel hasil', ['Semua kategori', *LABELS.values(), 'Tidak valid'])
    filtered = output if category == 'Semua kategori' else output.loc[~valid] if category == 'Tidak valid' else output[output['Prediksi_Kategori'] == category]
    st.dataframe(filtered, hide_index=True, width='stretch')
    st.download_button('Unduh seluruh hasil CSV', data=safe_csv_bytes(output),
                       file_name='Hasil_Deteksi_SMS.csv', mime='text/csv', type='primary')
    st.caption('Unduhan selalu mencakup seluruh baris. Karakter pemicu formula spreadsheet dinetralkan pada teks ekspor.')


def matrix_plot(model):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    cm = np.array(model['test']['confusion_matrix'])
    fig, ax = plt.subplots(figsize=(5, 3.6))
    cmap = LinearSegmentedColormap.from_list('forest', ['#eff5f0', '#236447'])
    ax.imshow(cm, cmap=cmap, vmin=0)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', fontsize=14,
                    color='white' if cm[i, j] > cm.max()/2 else '#162d25')
    ax.set_xticks(range(3), list(LABELS.values()))
    ax.set_yticks(range(3), list(LABELS.values()))
    ax.set_xlabel('Kategori prediksi', labelpad=10)
    ax.set_ylabel('Kategori aktual', labelpad=10)
    ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    fig.tight_layout()
    try:
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=160, bbox_inches='tight')
        st.html(png_markup(buffer.getvalue(), f"Confusion matrix {model['model_name']}"))
    finally:
        plt.close(fig)


def model_dashboard():
    intro('Lihat bukti di balik prediksi.', 'Perbandingan tiga algoritma, data uji terpisah, dan batasan yang perlu dipahami.')
    a, b, c, d = st.columns(4)
    a.metric('SMS Indonesia', f"{INDO['dataset_rows']:,}")
    b.metric('Data latih / uji', f"{INDO['train_rows']} / {INDO['test_rows']}")
    c.metric('Macro-F1 uji terpilih', percent(SELECTED['test']['f1_macro']))
    d.metric('Recall Penipuan', percent(SELECTED['test']['per_class']['Penipuan']['recall']))
    st.subheader('Perbandingan model Indonesia')
    st.caption('Model dipilih dari rata-rata macro-F1 5-fold CV data latih; recall Penipuan menjadi pemecah seri. TF-IDF dipelajari ulang dalam setiap fold.')
    rows = []
    for model in INDO['models']:
        test = model['test']
        rows.append({'Algoritma': model['model_name'], 'Pilihan': 'Model utama' if model['model_name'] == INDO['selected_model'] else 'Pembanding',
                     'CV Macro-F1': f"{model['cv_f1_macro_mean']:.4f} ± {model['cv_f1_macro_std']:.4f}",
                     'Akurasi uji': percent(test['accuracy']), 'Precision macro': percent(test['precision_macro']),
                     'Recall macro': percent(test['recall_macro']), 'Macro-F1 uji': percent(test['f1_macro']),
                     'Recall Penipuan': percent(test['per_class']['Penipuan']['recall'])})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch')
    st.info(f"Model utama: {INDO['selected_model']}. Rata-rata CV macro-F1 {SELECTED['cv_f1_macro_mean']:.4f}. Data uji baru dinilai setelah pemilihan model.")
    model_name = st.selectbox('Tinjau hasil algoritma', [m['model_name'] for m in INDO['models']],
                              index=[m['model_name'] for m in INDO['models']].index(INDO['selected_model']))
    model = next(m for m in INDO['models'] if m['model_name'] == model_name)
    left, right = st.columns([1, 1.1], gap='large')
    with left:
        st.subheader('Confusion matrix')
        matrix_plot(model)
        cm = model['test']['confusion_matrix']
        missed = sum(cm[1]) - cm[1][1]
        st.caption(f'{missed} dari {sum(cm[1])} pesan Penipuan pada data uji diprediksi sebagai kategori lain. Baris = aktual; kolom = prediksi.')
    with right, st.container(key='model_detail'):
        st.subheader('Metrik per kategori')
        records = [{'Kategori': name, 'Precision': percent(vals['precision']), 'Recall': percent(vals['recall']),
                    'F1': percent(vals['f1']), 'Jumlah uji': vals['support']}
                   for name, vals in model['test']['per_class'].items()]
        st.dataframe(pd.DataFrame(records), hide_index=True, width='stretch')
        st.write('Perbandingan latih dan uji')
        train_f1, test_f1 = model['train']['f1_macro'], model['test']['f1_macro']
        st.write(f'Macro-F1 latih **{percent(train_f1)}** · uji **{percent(test_f1)}**')
        st.caption(f'Selisih {(train_f1-test_f1)*100:.2f} poin persentase. Selisih ini adalah indikasi pada satu split; belum membuktikan generalisasi pada pesan baru.')
    with st.expander('Dataset dan metodologi', expanded=False):
        l, r = st.columns(2)
        with l:
            st.write('Data utama Indonesia')
            st.write('1.143 SMS mentah menjadi 1.138 pesan bersih. Sumber: korpus SMS Yudi Wibisono. Tiga kelas tetap mengikuti anotasi dataset.')
            st.dataframe(pd.DataFrame([{'Kelas': name, 'Jumlah': amount} for name, amount in INDO['class_distribution'].items()]), hide_index=True)
        with r:
            st.write('Alur eksperimen')
            st.write('Stratified split 80:20, seed 42. Kandidat memakai TF-IDF unigram dan bigram, sublinear TF. Validasi silang 5 fold dilakukan pada data latih. Heuristik ditampilkan sebagai informasi terpisah.')
            en = EVALUATION['english']
            st.write(f"Inggris: {en['dataset_rows']:,} pesan unik terpilih; {en['train_rows']:,} latih / {en['test_rows']:,} uji. Akurasi {percent(en['test']['accuracy'])}, macro-F1 {percent(en['test']['f1_macro'])}.")
            st.caption('Kategori Inggris yang terlalu umum dikeluarkan. Asal korpus Inggris masih perlu diverifikasi; hasilnya bersifat eksploratif.')
    with st.expander('Eksplorasi data (EDA)'):
        plots = {'Distribusi kelas': '1_class_distribution.png', 'Panjang pesan': '2_length_distribution.png',
                 'Indikator heuristik': '3_heuristic_indicators.png', 'Kata kunci': '4_top_keywords.png',
                 'Korelasi fitur': '5_correlation_heatmap.png',
                 'Kata berpengaruh pada model': 'feature_importance.png'}
        plot = st.selectbox('Pilih visualisasi', list(plots))
        st.html(png_markup((ROOT / 'eda_results' / plots[plot]).read_bytes(), plot))
        if plot == 'Kata berpengaruh pada model':
            st.caption('Bobot fitur model Indonesia terpilih. Pada SVM terkalibrasi, bobot dirata-ratakan dari estimator; ini bukan penjelasan kausal.')
        else:
            st.caption('EDA menggunakan korpus standar sebelum seleksi kategori Inggris untuk training. Jumlah korpus EDA Inggris berbeda dari jumlah data model Inggris.')
    with st.expander('Keterbatasan dan analisis kesalahan'):
        st.write('Data Indonesia relatif kecil dan lama. Bahasa campuran, ejaan tersamarkan, pesan sangat pendek, serta modus baru dapat menurunkan ketepatan. Belum ada validasi eksternal dengan SMS Indonesia terbaru.')
        error_path = ROOT / 'models/error_analysis.csv'
        if error_path.exists():
            st.dataframe(pd.read_csv(error_path), hide_index=True, width='stretch')
    st.download_button('Unduh data evaluasi JSON', data=(ROOT / 'models/evaluation.json').read_bytes(),
                       file_name='evaluasi_smishingguard.json', mime='application/json')


def education():
    intro('Baca polanya. Periksa konteksnya.', 'Kenali taktik yang mendorong Anda bertindak cepat sebelum sempat memeriksa.')
    cases = [
        ('Hadiah & undian', 'Menang tanpa pernah ikut?', 'Nama merek, nominal hadiah besar, dan batas klaim singkat dapat dipakai untuk meminta biaya, data rekening, atau OTP.',
         'Selamat! Anda terpilih mendapat hadiah Rp 100 juta. Klaim segera, hubungi 081234567890 dan kirim data rekening Anda.'),
        ('Kurir & berkas APK', 'Paket menjadi alasan mengunduh.', 'Permintaan memasang aplikasi dari pesan perlu diperiksa. Nama kurir pada pesan saja tidak mengesahkan identitas pengirim.',
         'Paket Anda tertahan karena alamat kurang lengkap. Silakan unduh berkas resi-paket.apk melalui tautan yang kami kirim.'),
        ('Akun & rekening', 'Ancaman pemblokiran mendadak.', 'Pesan yang meminta verifikasi kredensial dengan mendesak dapat meniru komunikasi bank. Buka aplikasi resmi secara mandiri.',
         'PERINGATAN! Rekening Anda akan diblokir hari ini. Segera kirim OTP untuk verifikasi akun dan data rekening.'),
        ('Pinjaman & dana tunai', 'Penawaran yang terlalu mudah.', 'Janji pencairan cepat, syarat minim, dan biaya awal perlu ditinjau. Sebuah penawaran belum tentu berasal dari pihak yang disebutkan.',
         'Pinjaman tunai langsung cair tanpa jaminan. Hubungi WA 081234567890. Transfer biaya administrasi agar dana masuk ke rekening Anda.'),
    ]
    for start in range(0, len(cases), 2):
        cols = st.columns(2, gap='large')
        for col, (kind, title, body, sample) in zip(cols, cases[start:start+2]):
            with col:
                st.html(f'<article class="education-card"><div class="case-type">{kind}</div><h3>{title}</h3><p>{body}</p></article>')
                with st.expander(f'Contoh ilustratif: {kind}'):
                    st.code(sample, language=None, wrap_lines=True)
                    st.caption('Contoh edukasi. Gunakan pemindai untuk mencoba; model dapat salah pada pola yang belum dipelajari.')
    st.divider()
    left, right = st.columns(2, gap='large')
    with left:
        st.subheader('Jeda sebelum menindaklanjuti')
        st.markdown('- Periksa konteks: apakah Anda mengenal pengirim dan menunggu pesan ini?\n- Cari kontak resmi secara mandiri; jangan memakai kontak dalam pesan yang diragukan.\n- Simpan bukti pesan jika perlu ditinjau atau dilaporkan.\n- Jangan membagikan OTP, PIN, atau kata sandi melalui SMS.')
    with right:
        st.subheader('Cara kerja SmishingGuard')
        steps = [('Teks dibersihkan', 'Normalisasi singkatan dan penyamaran URL, nomor, nominal, serta kode layanan.'),
                 ('Pola kata dipetakan', 'TF-IDF mengubah kata dan pasangan kata menjadi fitur numerik.'),
                 ('Model mengklasifikasikan', 'Model terlatih memberi probabilitas untuk Normal, Penipuan, dan Promosi.'),
                 ('Anda menilai konteks', 'Gunakan skor, kata berpengaruh, dan indikator sebagai bahan pemeriksaan awal.')]
        st.html(''.join(f'<div class="method-step"><strong>{title}</strong><p>{body}</p></div>' for title, body in steps))


st.html(f'''<div class="brandbar"><div class="brand">{SHIELD}<div>Smishing<span>Guard</span></div></div>
<div class="brand-meta"><span>Proyek Machine Learning · SV IPB</span><span class="pill">Analisis SMS berbasis NLP</span></div></div>
<section class="hero"><div class="liquid" aria-hidden="true"></div><div class="hero-main"><div>
<div class="eyebrow">Berhenti sejenak. Periksa pesannya.</div><h1>Pesan masuk.<br><em>Jangan buru-buru percaya.</em></h1>
<p class="hero-copy">Bantu kenali pola SMS penipuan, promosi, dan percakapan biasa. Periksa pesannya, pahami alasannya, tentukan langkah berikutnya.</p>
<div class="hero-tags"><span>{CHECK}Indonesia & English</span><span>{CHECK}Tanpa menyimpan SMS ke disk</span></div></div>
<div class="hero-art" aria-hidden="true"><div class="orbit"></div><div class="message-preview"><div class="preview-head"><span class="preview-symbol">SMS</span><span>Satu pesan, banyak petunjuk</span></div><div class="preview-line"></div><div class="preview-line short"></div><div class="preview-line"></div><div class="preview-classes"><span>Normal</span><span>Penipuan</span><span>Promosi</span></div></div><div class="shield-float" style="color:#a8cbb3">{SHIELD}</div></div></div>
<div class="hero-stats"><div><strong>{INDO['dataset_rows']:,}</strong><small>SMS Indonesia bersih</small></div><div><strong>{percent(SELECTED['test']['accuracy'])}</strong><small>Akurasi pada {INDO['test_rows']} SMS uji</small></div><div><strong>3 algoritma</strong><small>Dibandingkan dengan 5-fold CV</small></div><div><strong>{INDO['selected_model']}</strong><small>Model Indonesia terpilih</small></div></div></section>''')

single_tab, batch_tab, model_tab, education_tab = st.tabs(['Pemindai SMS', 'Pemeriksaan CSV', 'Tentang model', 'Panduan smishing'])
with single_tab:
    scanner()
with batch_tab:
    batch()
with model_tab:
    model_dashboard()
with education_tab:
    education()

st.html('<div class="footer"><span><strong>SmishingGuard</strong> · Proyek klasifikasi SMS dengan Machine Learning</span><span>Alat bantu membaca pola. Keamanan pesan tetap perlu diverifikasi.</span></div>')
