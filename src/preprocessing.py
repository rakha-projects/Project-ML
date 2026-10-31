"""
Modul Preprocessing, Normalisasi Teks, dan Deteksi Bahasa SMS (Indonesia & Inggris).
Mendukung pembersihan data latih dwibahasa dan inferensi interaktif pada aplikasi web.
"""

import re
from typing import List, Dict, Any, Union, Tuple

# ==============================================================================
# 1. KAMUS NORMALISASI SINGKATAN & SLANG (INDONESIA & INGGRIS)
# ==============================================================================

ID_SLANG_DICTIONARY: Dict[str, str] = {
    # Kata ganti & kata hubung umum
    "sy": "saya", "aq": "saya", "gw": "saya", "gue": "saya",
    "km": "kamu", "kmu": "kamu", "lu": "kamu", "lo": "kamu",
    "dy": "dia", "mrk": "mereka", "qt": "kita", "qta": "kita",
    "org": "orang", "kpd": "kepada", "dr": "dari", "dgn": "dengan", "dg": "dengan",
    "utk": "untuk", "buat": "untuk", "bg": "bagi", "dlm": "dalam", "pd": "pada",
    "tsb": "tersebut", "m-dptkan": "dapatkan", "m-dpt": "dapat", "dptkan": "dapatkan",
    "dpt": "dapat", "sdh": "sudah", "udh": "sudah", "dah": "sudah",
    "blm": "belum", "lom": "belum", "tdk": "tidak", "tak": "tidak",
    "ga": "tidak", "gak": "tidak", "g": "tidak", "ngga": "tidak", "nggak": "tidak",
    "ndak": "tidak", "bkn": "bukan", "tp": "tapi", "tpi": "tapi",
    "krn": "karena", "karna": "karena", "jg": "juga", "jga": "juga",
    "plg": "pelanggan", "yth": "yang terhormat", "yg": "yang", "sbg": "sebagai",
    "bgt": "banget", "bgtt": "banget", "bener": "benar", "beneran": "benar",
    "bnr": "benar", "bs": "bisa", "bsa": "bisa", "cb": "coba", "cba": "coba",
    "msh": "masih", "msih": "masih", "skrg": "sekarang", "skrng": "sekarang",
    "bsk": "besok", "kemaren": "kemarin", "kmrn": "kemarin", "lgsg": "langsung",
    "lgsung": "langsung", "sm": "sama", "d": "di", "ke": "ke",

    # Istilah komunikasi & transaksi SMS Indonesia
    "hub": "hubungi", "hubungin": "hubungi", "call": "hubungi",
    "tlp": "telepon", "telp": "telepon", "no": "nomor", "nmr": "nomor",
    "rek": "rekening", "rekening": "rekening", "kirim": "kirim", "krm": "kirim",
    "info": "informasi", "inpo": "informasi", "dftr": "daftar", "reg": "daftar",
    "unreg": "berhenti", "aktif": "aktif", "aktifkan": "aktifkan",
    "buruan": "segera", "segera": "segera", "grts": "gratis", "free": "gratis",
    "disc": "diskon", "discn": "diskon", "dscn": "diskon",
    "slmt": "selamat", "selamet": "selamat", "pemenang": "pemenang",
    "menang": "menang", "hadiah": "hadiah", "undian": "undian",
    "gebyar": "undian", "klaim": "klaim", "ambil": "ambil",

    # Istilah pinjaman & penipuan finansial (Pinjol/Fraud)
    "pinjam": "pinjaman", "pinjaman": "pinjaman", "kta": "pinjaman",
    "cc": "kartu kredit", "kartu": "kartu", "dana": "dana", "tunai": "tunai",
    "cair": "cair", "bunga": "bunga", "angsuran": "cicilan", "cicilan": "cicilan",
    "syarat": "syarat", "ktp": "kartu tanda penduduk", "bpkb": "pinjaman jaminan bpkb",
    "byr": "bayar", "min": "minimal", "lunas": "lunas", "pelunasan": "pelunasan",
    "resmi": "resmi", "legal": "resmi", "shopee": "shopee", "lazada": "lazada",
    "tokopedia": "tokopedia", "bank": "bank", "bca": "bank bca", "bri": "bank bri",
    "bni": "bank bni", "mandiri": "bank mandiri",

    # Istilah operator seluler & kuota
    "kuota": "kuota", "kuo": "kuota", "flash": "flash", "paket": "paket",
    "pulsa": "pulsa", "plsa": "pulsa", "gb": "gigabyte", "mb": "megabyte",
    "kb": "kilobyte", "mnt": "menit", "hr": "hari", "bln": "bulan", "thn": "tahun",
    "rb": "ribu", "ribu": "ribu", "jt": "juta", "juta": "juta", "rp": "rupiah",
    "sd": "sampai dengan", "s/d": "sampai dengan", "app": "aplikasi", "apps": "aplikasi",
    "download": "unduh", "unduh": "unduh", "tsel": "telkomsel", "mytsel": "mytelkomsel",
    "indosat": "indosat", "xl": "xl", "tri": "tri", "axis": "axis", "smartfren": "smartfren",
    "s&k": "syarat dan ketentuan"
}

EN_SLANG_DICTIONARY: Dict[str, str] = {
    # Pronouns, Contractions & General SMS Slang
    "u": "you", "ur": "your", "urs": "yours", "4u": "for you", "4": "for", "2": "to",
    "b": "be", "c": "see", "r": "are", "y": "why", "m8": "mate", "msg": "message",
    "txt": "text", "txts": "texts", "pls": "please", "plz": "please", "thx": "thanks",
    "thanx": "thanks", "asap": "as soon as possible", "w/": "with", "w/o": "without",
    "idk": "i do not know", "dunno": "do not know", "gonna": "going to",
    "wanna": "want to", "gotta": "got to", "im": "i am", "dont": "do not",
    "cant": "cannot", "wont": "will not", "isnt": "is not", "arent": "are not",
    "havent": "have not", "hasnt": "has not", "hadnt": "had not", "didnt": "did not",
    "wouldnt": "would not", "couldnt": "could not", "shouldnt": "should not",
    "wkly": "weekly", "comp": "competition", "tkts": "tickets", "min": "minute",
    "mins": "minutes", "sec": "seconds", "hr": "hour", "hrs": "hours",
    "info": "information", "cust": "customer", "acc": "account", "ph": "phone",
    "tel": "telephone", "mob": "mobile", "rcvd": "received", "std": "standard",
    "pm": "private message", "tc": "terms and conditions", "t&cs": "terms and conditions"
}

# Gabungan kamus untuk fallback
UNIVERSAL_SLANG = {**ID_SLANG_DICTIONARY, **EN_SLANG_DICTIONARY}

# ==============================================================================
# 2. DETEKSI BAHASA (LANGUAGE DETECTION ENGINE)
# ==============================================================================

ID_STOPWORDS = {
    'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'pada', 'adalah',
    'dengan', 'saya', 'kamu', 'anda', 'bisa', 'sudah', 'tidak', 'ada', 'oleh',
    'karena', 'selamat', 'pulsa', 'kuota', 'rupiah', 'ribu', 'juta', 'hubungi',
    'rekening', 'nomor', 'pelanggan', 'paket', 'promo', 'penipuan', 'kirim',
    'besok', 'hari', 'bulan', 'tahun', 'dapat', 'belum', 'terima', 'kasih',
    'sy', 'dpt', 'utk', 'kpd', 'tsel', 'rek', 'yg', 'sdh', 'blm', 'bsk', 'tp', 'jg',
    'cair', 'pinjaman', 'kta', 'angsuran', 'cicilan', 'bunga', 'pemenang', 'undian'
}

EN_STOPWORDS = {
    'the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'for', 'you', 'it',
    'with', 'as', 'be', 'on', 'at', 'by', 'this', 'have', 'from', 'free',
    'call', 'text', 'now', 'urgent', 'claim', 'win', 'reply', 'stop', 'contact',
    'won', 'cash', 'prize', 'today', 'mobile', 'customer', 'service', 'account',
    'your', 'our', 'we', 'are', 'please', 'ur', 'txt', 'msg', 'pls', 'entry',
    'winner', 'selected', 'award', 'apply', 'loan', 'credit', 'rate', 'guaranteed'
}

def detect_language(text: str) -> Dict[str, Any]:
    """
    Mendeteksi apakah pesan SMS berbahasa Indonesia atau Inggris secara otomatis.
    Mengembalikan nama bahasa, kode bahasa ('id' / 'en'), dan skor keyakinan.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "language": "id",
            "language_name": "Indonesia (Default)",
            "confidence": 0.50,
            "id_score": 0,
            "en_score": 0
        }

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return {
            "language": "id",
            "language_name": "Indonesia (Default)",
            "confidence": 0.50,
            "id_score": 0,
            "en_score": 0
        }

    id_hits = sum(1 for w in words if w in ID_STOPWORDS)
    en_hits = sum(1 for w in words if w in EN_STOPWORDS)

    total_hits = id_hits + en_hits
    if total_hits == 0:
        # Fallback jika kata terlalu pendek / umum
        return {
            "language": "id",
            "language_name": "Indonesia (Otomatis)",
            "confidence": 0.51,
            "id_score": 0,
            "en_score": 0
        }

    if id_hits >= en_hits:
        conf = round(id_hits / total_hits, 2)
        return {
            "language": "id",
            "language_name": "Bahasa Indonesia",
            "confidence": conf,
            "id_score": id_hits,
            "en_score": en_hits
        }
    else:
        conf = round(en_hits / total_hits, 2)
        return {
            "language": "en",
            "language_name": "English (Bahasa Inggris)",
            "confidence": conf,
            "id_score": id_hits,
            "en_score": en_hits
        }

# ==============================================================================
# 3. POLA REGULAR EXPRESSION MULTI-BAHASA
# ==============================================================================

URL_PATTERN = re.compile(
    r'(?:https?:\/\/|www\.)[^\s/$.?#].[^\s]*|'
    r'\b(?:tsel\.me|bit\.ly|tinyurl\.com|s\.id|cutt\.ly|goo\.gl|t\.co|ow\.ly|is\.gd)\/[^\s]+|'
    r'\b[a-zA-Z0-9-]+\.(?:com|me|id|xyz|tk|ml|top|net|org|co|info|site|uk|us)\/[^\s]*',
    re.IGNORECASE
)

# Mendukung nomor Indonesia (+62 / 08...) dan Inggris/Internasional (0800, 0905, 07..., +44...)
PHONE_PATTERN = re.compile(
    r'(?:\+?62|08)[0-9]{8,12}\b|'
    r'(?:\+?44|0)[789][0-9]{8,10}\b|'
    r'\b0800[0-9]{6,7}\b|\b0905[0-9]{6,7}\b|\b0906[0-9]{6,7}\b|'
    r'\(wa\)\s*(?:\+?62|08)[0-9]{8,12}|'
    r'(?:wa|hub|hubungi|call|contact|text|ring)\s*[:.-]?\s*(?:\+?[0-9-]{8,15})',
    re.IGNORECASE
)

# Mendukung mata uang Rupiah (Rp, IDR, jt, rb), Dollar ($), Poundsterling (£), Euro (€), Pence (p)
NOMINAL_PATTERN = re.compile(
    r'(?:rp\.?|idr)\s*[\d\.,]+(?:\s*(?:jt|juta|ribu|rb))?|'
    r'[\$£€]\s*[\d\.,]+(?:\s*(?:k|million|m|thousand))?|'
    r'\b\d+\s*(?:jt|juta|ribu|rb|pounds|pence|p|usd|gbp|eur)\b',
    re.IGNORECASE
)

SHORTCODE_PATTERN = re.compile(
    r'\*[0-9#*]{3,12}#|\b[0-9]{5,6}\b',  # USSD kode *363# atau SMS shortcode 5 digit (misal: 83049)
    re.IGNORECASE
)

TIMESTAMP_PATTERN = re.compile(
    r'\b\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.?|\b\d{1,2}\/\d{1,2}\/\d{2,4}\b',
    re.IGNORECASE
)

# ==============================================================================
# 4. EKSTRAKSI HEURISTIK RISIKO (INDONESIA & INGGRIS)
# ==============================================================================

def extract_heuristic_features(text: str, lang: str = "auto") -> Dict[str, Any]:
    """
    Mengekstrak indikator keamanan heuristik dari teks SMS mentah (Indonesia & Inggris).
    """
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    text_lower = text.lower()

    if lang == "auto":
        detected = detect_language(text)
        current_lang = detected["language"]
    else:
        current_lang = lang

    # 1. Deteksi URL / Tautan
    urls_found = URL_PATTERN.findall(text)
    has_url = len(urls_found) > 0

    # 2. Deteksi Kontak / Nomor Telepon
    phones_found = PHONE_PATTERN.findall(text)
    has_phone = len(phones_found) > 0

    # 3. Deteksi Nominal Uang
    nominals_found = NOMINAL_PATTERN.findall(text)
    has_nominal = len(nominals_found) > 0

    # 4. Deteksi Kode USSD / Shortcode
    codes_found = SHORTCODE_PATTERN.findall(text)
    has_shortcode = len(codes_found) > 0

    # 5. Kata Kunci Urgensi (Sense of Urgency)
    urgency_id = [
        "buruan", "segera", "sekarang juga", "hari ini", "terpilih", "spesial",
        "terbatas", "sebelum terlambat", "peringatan", "diblokir", "kartu anda"
    ]
    urgency_en = [
        "urgent", "immediately", "hurry", "expires", "warning", "limited time",
        "act now", "today only", "deadline", "suspended", "action required"
    ]
    urgency_list = urgency_id if current_lang == "id" else urgency_en
    detected_urgency = [w for w in urgency_list if w in text_lower]

    # 6. Kata Kunci Finansial & Pancingan Phishing
    financial_id = [
        "pinjaman", "kta", "tanpa jaminan", "cair", "bunga", "lunas", "kartu kredit",
        "hadiah", "pemenang", "cek tunai", "undian", "pin", "rekening", "transfer",
        "otp", "klaim", "shopee", "lazada", "bpkb"
    ]
    financial_en = [
        "won", "winner", "prize", "claim", "cash", "lottery", "free", "credit card",
        "bank", "account", "crypto", "bitcoin", "refund", "deposit", "guaranteed",
        "congratulations", "gift card", "voucher", "verify"
    ]
    financial_list = financial_id if current_lang == "id" else financial_en
    detected_financial = [w for w in financial_list if w in text_lower]

    # 7. Perhitungan Skor Risiko Heuristik (0 - 100)
    risk_score = 0
    if has_url:
        risk_score += 35
    if has_phone:
        risk_score += 20
    if has_nominal:
        risk_score += 15
    if detected_urgency:
        risk_score += 15
    if detected_financial:
        risk_score += 25
    if has_shortcode and not has_url and not has_phone:
        # Kode dial USSD (*363#) tanpa link biasanya promo operator normal
        risk_score = max(0, risk_score - 25)

    risk_score = min(100, risk_score)

    return {
        "text_length": len(text),
        "word_count": len(text.split()),
        "language": current_lang,
        "has_url": has_url,
        "urls_detected": urls_found,
        "has_phone": has_phone,
        "phones_detected": phones_found,
        "has_nominal": has_nominal,
        "nominals_detected": nominals_found,
        "has_shortcode": has_shortcode,
        "codes_detected": codes_found,
        "urgency_keywords": detected_urgency,
        "financial_keywords": detected_financial,
        "heuristic_risk_score": risk_score
    }

# ==============================================================================
# 5. PEMBERSIHAN & NORMALISASI TEKS (CLEAN TEXT)
# ==============================================================================

def normalize_slang(text: str, lang: str = "id") -> str:
    """
    Mengganti kata singkatan / slang dengan bentuk bakunya berdasarkan bahasa.
    """
    dict_to_use = ID_SLANG_DICTIONARY if lang == "id" else EN_SLANG_DICTIONARY
    words = text.split()
    normalized_words = [dict_to_use.get(w, w) for w in words]
    return " ".join(normalized_words)


def clean_text(text: str, lang: str = "auto") -> str:
    """
    Pipeline lengkap pembersihan teks SMS (Indonesia & Inggris):
    1. Deteksi Bahasa (jika 'auto')
    2. Lowercase (Case Folding)
    3. Hapus timestamp otomatis
    4. Entity Masking: [url], [kode], [nomor], [nominal]
    5. Hapus karakter non-alphanumeric selain token placeholder
    6. Normalisasi singkatan SMS sesuai bahasa
    7. Perapihan whitespace
    """
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    if lang == "auto":
        detected = detect_language(text)
        current_lang = detected["language"]
    else:
        current_lang = lang

    # 1. Lowercase (Case Folding)
    text = text.lower()

    # 2. Hapus timestamp otomatis
    text = TIMESTAMP_PATTERN.sub(" ", text)

    # 3. Masking Entity
    text = URL_PATTERN.sub(" [url] ", text)
    text = SHORTCODE_PATTERN.sub(" [kode] ", text)
    text = PHONE_PATTERN.sub(" [nomor] ", text)
    text = NOMINAL_PATTERN.sub(" [nominal] ", text)

    # 4. Hapus karakter non-alfanumerik selain kurung siku token
    text = re.sub(r'[^a-z0-9\[\]\s]', ' ', text)

    # 5. Normalisasi Singkatan SMS
    text = normalize_slang(text, lang=current_lang)

    # 6. Rapikan spasi ganda
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def batch_clean_text(texts: List[str], lang: str = "auto") -> List[str]:
    """
    Memproses kumpulan teks SMS dalam format list secara efisien.
    """
    return [clean_text(t, lang=lang) for t in texts]


if __name__ == "__main__":
    # Verifikasi modul preprocessing bilingual
    samples = [
        # 1. Normal Indonesia
        "Besok kuliah jam 8 di lab komputer jangan lupa bawa laptop ya bro",
        # 2. Promosi Indonesia
        "[PROMO] Beli paket Flash mulai 1GB di MY TELKOMSEL APP dpt EXTRA kuota 2GB 4G LTE. Buruan, cek di tsel.me/mytsel1 S&K *363#",
        # 3. Penipuan Indonesia
        "Selamat No anda m-dptkan Cek Tunai 100jt dr Shopee. PIN: 254F77 Hub WA: 082134976289 atau klik http://shopee-klaim.xyz/dana Segera lapor rek anda!",
        # 4. Normal Inggris
        "Hey mate, are you coming to the football match tonight? Let me know asap.",
        # 5. Promosi Inggris
        "Special offer 4u! Get a brand new video phone with 150 free text and 750 mins for only 5 pounds per week. Reply delivery tomorrow.",
        # 6. Penipuan Inggris
        "URGENT! You have won a 1000 cash prize or 1 week holiday to Hawaii! Call 09061701461 to claim your reward now. Terms apply."
    ]

    print("=" * 70)
    print("PENGUJIAN MODUL PREPROCESSING & DETEKSI BAHASA (BILINGUAL)")
    print("=" * 70)

    for i, s in enumerate(samples, 1):
        det = detect_language(s)
        cleaned = clean_text(s, lang=det["language"])
        heur = extract_heuristic_features(s, lang=det["language"])
        print(f"\n[Sampel {i}]")
        print(f"Bahasa   : {det['language_name']} (Confidence: {det['confidence']*100:.0f}%)")
        print(f"Raw      : {s}")
        print(f"Cleaned  : {cleaned}")
        print(f"Heuristik: Risk={heur['heuristic_risk_score']} | URL={heur['has_url']} | Phone={heur['has_phone']} | Nominal={heur['has_nominal']}")
        print(f"Keywords : Urgensi={heur['urgency_keywords']} | Finansial={heur['financial_keywords']}")
