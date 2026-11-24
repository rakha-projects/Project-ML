// ==============================================================================
// SMISHINGGUARD JAVASCRIPT ENGINE (SOLID COLOR, MULTILINGUAL ID & EN)
// Menu, Carousel, Tabs, Dual-Language Presets, and Hybrid AI Detection Simulator
// ==============================================================================

// 1. Mobile Menu Toggle
const burger = document.getElementById('burger');
const menu = document.getElementById('menu');
if (burger && menu) {
  burger.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));
}

// 2. Tab Filter for Real-World Cases
const tabs = document.querySelectorAll('.tab');
const cards = document.querySelectorAll('.card');
tabs.forEach(tab => tab.addEventListener('click', () => {
  tabs.forEach(t => t.classList.remove('active'));
  tab.classList.add('active');
  const filter = tab.dataset.f;
  cards.forEach(c => {
    if (filter === 'all') {
      c.hidden = false;
    } else {
      c.hidden = c.dataset.c !== filter;
    }
  });
}));

// 3. Carousel Navigation
const track = document.getElementById('track');
const step = () => (track.querySelector('.card:not([hidden])')?.offsetWidth || 320) + 20;
const nextBtn = document.getElementById('next');
const prevBtn = document.getElementById('prev');
if (nextBtn && track) {
  nextBtn.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
}
if (prevBtn && track) {
  prevBtn.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
}

// 4. Preset Cases Data (Indonesian & English - N=10.607 Corpus Supported)
const PRESETS = {
  // Indonesian Presets
  shopee: "Surat Keputusan Resmi Shopee 77: No. Anda terpilih pemenang Hadiah Cek Rp 175.000.000. Kode PIN: 254F77. Klaim hadiah segera hubungi WhatsApp di wa.me/6281298765432",
  apk: "Paket J&T Express tertahan di gudang drop point karena alamat kurang detail. Silakan unduh dan cek bukti foto paket Anda di: https://bit.ly/resi-paket-jnt.apk",
  pinjol: "KTA Dana Kilat: Dapatkan pinjaman tunai tanpa agunan s.d Rp 50.000.000, bunga 0%, cair 5 menit langsung ke rekening Anda. Info klik https://pinjol-kilat.id/acc atau WA 085712345678",
  promo: "Paket Flash Spesial! Nikmati Kuota 25GB berlaku 30 hari hanya Rp 50.000. Aktifkan sekarang di *363*88# atau kunjungi aplikasi MyTelkomsel. S&K berlaku.",
  normal: "Bro, besok pagi jam 9 kumpul di perpustakaan kampus ya buat selesaikan tugas akhir Machine Learning bareng kelompok.",
  
  // English Presets (Corpus Kaggle / International Smishing)
  en_lottery: "URGENT! You have won a £1,000 cash prize or a 2-week luxury holiday! Call 09061743835 from landline to claim your reward. Claim code: KL88. T&Cs apply.",
  en_bank: "SECURITY ALERT: Unusual sign-in attempt detected on your PayPal account from London, UK. If this was not you, verify identity at: https://bit.ly/secure-paypal-check",
  en_delivery: "Royal Mail: Your parcel has a £1.45 unpaid shipping fee and cannot be delivered. Update delivery preferences and pay online at: https://bit.ly/royalmail-redelivery-fee",
  en_promo: "SUMMER SPECIAL OFFER! Get 500 anytime minutes, free video phone and unlimited texts for only £20/month. Reply YES to 88066 to order today! Opt-out stop2end.",
  en_normal: "Hey mate, are you coming over to campus today? We need to finalize the machine learning presentation slides before 4pm."
};

const smsInput = document.getElementById('smsInput');
const charCount = document.getElementById('charCount');
const detectedLang = document.getElementById('detectedLang');
const langConfidence = document.getElementById('langConfidence');
const scanBtn = document.getElementById('scanBtn');
const clearBtn = document.getElementById('clearBtn');
const resultDisplay = document.getElementById('resultDisplay');

// Language Mode State ('auto', 'id', 'en')
let selectedLangMode = 'auto';

// Handle Language Mode Buttons
const modeButtons = document.querySelectorAll('.lang-mode-btn');
modeButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    modeButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedLangMode = btn.dataset.mode;
    updateTextMeta();
    if (smsInput.value.trim().length > 0) {
      runSmishingAnalysis(smsInput.value);
    }
  });
});

// Handle Preset Language Tabs (ID vs EN)
const presetTabButtons = document.querySelectorAll('.preset-tab');
const presetsId = document.getElementById('presetsId');
const presetsEn = document.getElementById('presetsEn');

presetTabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    presetTabButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.dataset.tab;
    if (tab === 'id') {
      presetsId.style.display = 'flex';
      presetsEn.style.display = 'none';
    } else {
      presetsId.style.display = 'none';
      presetsEn.style.display = 'flex';
    }
  });
});

// Vocabulary Dictionary for Fast Language Identification
const ID_WORDS = [
  'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'pada', 'adalah',
  'dengan', 'saya', 'kamu', 'anda', 'bisa', 'sudah', 'tidak', 'ada', 'oleh',
  'karena', 'selamat', 'pulsa', 'kuota', 'rupiah', 'ribu', 'juta', 'hubungi',
  'rekening', 'nomor', 'pelanggan', 'paket', 'promo', 'penipuan', 'kirim',
  'besok', 'hari', 'bulan', 'tahun', 'dapat', 'belum', 'terima', 'kasih',
  'cair', 'pinjaman', 'kta', 'bunga', 'pemenang', 'undian', 'cek', 'klaim',
  'tertahan', 'gudang', 'resi', 'diblokir', 'verifikasi', 'akun'
];

const EN_WORDS = [
  'the', 'is', 'at', 'which', 'on', 'for', 'you', 'your', 'free', 'win', 'won',
  'urgent', 'claim', 'cash', 'prize', 'call', 'reply', 'to', 'from', 'with',
  'and', 'this', 'that', 'have', 'has', 'are', 'was', 'were', 'will', 'text',
  'txt', 'stop', 'send', 'please', 'pls', 'week', 'day', 'today', 'tonight',
  'mate', 'thanks', 'thx', 'offer', 'account', 'customer', 'alert', 'verify',
  'bank', 'parcel', 'delivery', 'card', 'login', 'security', 'mins', 'phone'
];

// Detect Language and Confidence
function computeLanguage(text) {
  if (!text || text.trim().length === 0) {
    return { lang: 'id', conf: 100, isAuto: true };
  }

  const lower = text.toLowerCase();
  let idCount = 0;
  let enCount = 0;

  ID_WORDS.forEach(w => {
    if (new RegExp('\\b' + w + '\\b').test(lower)) idCount += 1.5;
  });
  EN_WORDS.forEach(w => {
    if (new RegExp('\\b' + w + '\\b').test(lower)) enCount += 1.5;
  });

  // Check currency & symbol indicators
  if (/[£$€]/.test(text)) enCount += 3;
  if (/rp\b|rupiah/i.test(text)) idCount += 3;
  if (/\b(wa\.me|mytelkomsel|shopee)\b/i.test(text)) idCount += 2;
  if (/\b(paypal|royal\s*mail|amazon|landline)\b/i.test(text)) enCount += 3;

  let activeLang = 'id';
  let conf = 85;

  if (selectedLangMode === 'id') {
    activeLang = 'id';
    conf = 100;
  } else if (selectedLangMode === 'en') {
    activeLang = 'en';
    conf = 100;
  } else {
    // Auto Mode
    if (enCount > idCount) {
      activeLang = 'en';
      conf = Math.min(99, Math.round(75 + (enCount / (enCount + idCount + 0.1)) * 24));
    } else if (idCount > enCount) {
      activeLang = 'id';
      conf = Math.min(99, Math.round(75 + (idCount / (idCount + enCount + 0.1)) * 24));
    } else {
      activeLang = 'id';
      conf = 65;
    }
  }

  return { lang: activeLang, conf, isAuto: selectedLangMode === 'auto' };
}

// Update Text Counter, Detected Language UI
function updateTextMeta() {
  const text = smsInput.value;
  charCount.textContent = `${text.length} karakter`;

  if (text.trim().length === 0) {
    if (selectedLangMode === 'auto') {
      detectedLang.textContent = "AUTO (INDONESIA)";
      detectedLang.className = "lang-badge";
      langConfidence.textContent = "Mode: Otomatis";
    } else if (selectedLangMode === 'id') {
      detectedLang.textContent = "MANUAL (INDONESIA)";
      detectedLang.className = "lang-badge";
      langConfidence.textContent = "Mode: Terkunci ID";
    } else {
      detectedLang.textContent = "MANUAL (ENGLISH)";
      detectedLang.className = "lang-badge en";
      langConfidence.textContent = "Mode: Terkunci EN";
    }
    return;
  }

  const { lang, conf, isAuto } = computeLanguage(text);

  if (lang === 'en') {
    detectedLang.textContent = isAuto ? `AUTO: ENGLISH (EN)` : `MANUAL: ENGLISH (EN)`;
    detectedLang.className = "lang-badge en";
    langConfidence.textContent = `Tingkat Keyakinan Bahasa: ${conf}%`;
  } else {
    detectedLang.textContent = isAuto ? `AUTO: INDONESIA (ID)` : `MANUAL: INDONESIA (ID)`;
    detectedLang.className = "lang-badge";
    langConfidence.textContent = `Tingkat Keyakinan Bahasa: ${conf}%`;
  }
}

smsInput.addEventListener('input', updateTextMeta);

// Preset Buttons Event
document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const type = btn.dataset.type;
    if (PRESETS[type]) {
      smsInput.value = PRESETS[type];
      // Auto adjust language mode or let auto-detect handle
      if (type.startsWith('en_') && selectedLangMode === 'id') {
        selectedLangMode = 'auto';
        modeButtons.forEach(b => b.classList.toggle('active', b.dataset.mode === 'auto'));
      }
      updateTextMeta();
      runSmishingAnalysis(smsInput.value);
    }
  });
});

// "Uji Kasus Ini" Buttons in Carousel
document.querySelectorAll('.use-case-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const text = btn.dataset.text;
    smsInput.value = text;
    updateTextMeta();
    document.getElementById('scanner').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => {
      runSmishingAnalysis(text);
    }, 400);
  });
});

// Clear Button
clearBtn.addEventListener('click', () => {
  smsInput.value = '';
  updateTextMeta();
  resultDisplay.classList.remove('show', 'scam', 'safe', 'promo');
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
});

// Scan Button Trigger
scanBtn.addEventListener('click', () => {
  const text = smsInput.value.trim();
  if (!text) {
    alert("Silakan masukkan teks SMS atau pilih salah satu tombol preset terlebih dahulu.");
    smsInput.focus();
    return;
  }
  runSmishingAnalysis(text);
});

// ==============================================================================
// 5. HYBRID AI & HEURISTIC ENGINE (Multilingual ID & EN In-Browser Inference)
// ==============================================================================
function runSmishingAnalysis(text) {
  const lower = text.toLowerCase();
  const { lang, conf } = computeLanguage(text);

  // Common Regex Heuristics
  const urlRegex = /(https?:\/\/[^\s]+|bit\.ly\/[^\s]+|wa\.me\/[^\s]+|tinyurl\.com\/[^\s]+|s\.id\/[^\s]+|[a-z0-9-]+\.(?:xyz|top|info|site|club|vip|online|app|icu|cyou|live|me|com|id|net|co\.uk)[^\s]*)/i;
  
  // Indonesian and International/UK Phone Numbers & Shortcodes
  const phoneRegex = /(?:\+?62|08)[0-9]{8,12}\b|(?:\+?44|0906|0800|07)[0-9]{7,10}\b|\b(?:88066|8007|85555|87077)\b/;
  
  // Indonesian & English Currency Expressions (£, $, €, Rp, Juta, Pounds)
  const moneyRegex = /(?:rp\.?\s*[\d\.,]+|\b\d+\s*(?:juta|jt|ribu|rb|miliar|m|usd|dolar|pounds?|gbp)\b|[£$€]\s*[\d\.,]+)/i;
  const ussdRegex = /\*[0-9]+(?:\*[0-9]+)*#/;

  const hasUrl = urlRegex.test(text);
  const hasPhone = phoneRegex.test(text);
  const hasMoney = moneyRegex.test(text);
  const hasUssd = ussdRegex.test(text);

  let scamScore = 0;
  let promoScore = 0;

  if (lang === 'en') {
    // English Corpus Analysis (Kaggle / Global Smishing)
    const enScamKeywords = [
      'urgent', 'won', 'winner', 'prize', 'claim', 'cash', 'call', 'holiday',
      'congratulations', 'award', 'suspended', 'security alert', 'unusual activity',
      'verify identity', 'action required', 'account locked', 'refund', 'wire transfer',
      'paypal', 'royal mail', 'unpaid fee', 'redelivery', 'unauthorized', 'password',
      'login', 'pin', 'bank', 'package', 'selected', 'guaranteed'
    ];

    const enPromoKeywords = [
      'promo', 'offer', 'deal', 'discount', 'mins', 'minutes', 'ringtone', 'voucher',
      'sale', 'subscribe', 'txt', 'reply', 'special offer', 'gift', 'order today',
      'half price', 'free video phone', 'unlimited texts', 'customer appreciation', 'opt-out'
    ];

    enScamKeywords.forEach(k => {
      if (lower.includes(k)) scamScore += 1.8;
    });
    if (hasUrl) scamScore += 3;
    if (hasPhone) scamScore += 2;
    if (hasMoney) scamScore += 2.5;
    if (lower.includes('0906') || lower.includes('claim code')) scamScore += 4;
    if (lower.includes('paypal') && hasUrl) scamScore += 4.5;
    if (lower.includes('royal mail') && hasUrl) scamScore += 4.5;

    enPromoKeywords.forEach(k => {
      if (lower.includes(k)) promoScore += 1.6;
    });
    if (lower.includes('reply yes') || lower.includes('stop2end')) promoScore += 3.5;

  } else {
    // Indonesian Analysis (ID Dataset N=1.138)
    const idScamKeywords = [
      'undian', 'hadiah', 'shopee', 'pinjaman', 'dana kilat', 'tanpa agunan', 'cek', 'pemenang',
      'surat keputusan', 'rekening', 'diblokir', 'verifikasi akun', 'apk', 'paket tertahan',
      'bunga 0%', 'cair', 'klaim', 'pin', 'bca', 'bri', 'mandiri', 'link', 'klik'
    ];

    const idPromoKeywords = [
      'promo', 'kuota', 'gb', 'paket', 'flash', 'diskon', 'telkomsel', 'indosat', 'xl',
      'berlaku', 'aktifkan', 'mytelkomsel', 'tarif', 'cashback', 'voucher'
    ];

    idScamKeywords.forEach(k => {
      if (lower.includes(k)) scamScore += 1.5;
    });
    if (hasUrl) scamScore += 3;
    if (hasPhone) scamScore += 2;
    if (hasMoney) scamScore += 2.5;
    if (lower.includes('.apk')) scamScore += 5;

    idPromoKeywords.forEach(k => {
      if (lower.includes(k)) promoScore += 1.5;
    });
    if (hasUssd) promoScore += 4;
  }

  let verdict = "NORMAL";
  let pScam = 0.01;
  let pSafe = 0.98;
  let pPromo = 0.01;

  if (scamScore >= 3.8 || lower.includes('.apk') || (hasUrl && hasMoney) || (hasPhone && (lower.includes('won') || lower.includes('selamat')))) {
    verdict = "PENIPUAN";
    pScam = Math.min(0.99, 0.86 + (scamScore * 0.018));
    pSafe = Math.max(0.005, (1 - pScam) * 0.4);
    pPromo = 1 - pScam - pSafe;
  } else if (promoScore >= 3 || (hasUssd && lower.includes('kuota')) || lower.includes('reply yes')) {
    verdict = "PROMOSI";
    pPromo = Math.min(0.98, 0.82 + (promoScore * 0.028));
    pSafe = Math.max(0.01, (1 - pPromo) * 0.6);
    pScam = 1 - pPromo - pSafe;
  } else {
    verdict = "NORMAL";
    pSafe = 0.985;
    pScam = 0.009;
    pPromo = 0.006;
  }

  displayResults(verdict, pScam, pSafe, pPromo, hasUrl, hasPhone, hasMoney, hasUssd, lower, lang);
}

function displayResults(verdict, pScam, pSafe, pPromo, hasUrl, hasPhone, hasMoney, hasUssd, lower, lang) {
  resultDisplay.className = 'result-display show';

  const resultVerdict = document.getElementById('resultVerdict');
  const resultSub = document.getElementById('resultSub');
  const scoreBadge = document.getElementById('scoreBadge');
  const adviceTitle = document.getElementById('adviceTitle');
  const adviceText = document.getElementById('adviceText');

  const scamPct = Math.round(pScam * 100);
  const safePct = Math.round(pSafe * 100);
  const promoPct = Math.round(pPromo * 100);

  document.getElementById('scamPct').textContent = `${scamPct}%`;
  document.getElementById('scamBar').style.width = `${scamPct}%`;

  document.getElementById('safePct').textContent = `${safePct}%`;
  document.getElementById('safeBar').style.width = `${safePct}%`;

  document.getElementById('promoPct').textContent = `${promoPct}%`;
  document.getElementById('promoBar').style.width = `${promoPct}%`;

  const cardUrl = document.getElementById('cardUrl');
  const cardPhone = document.getElementById('cardPhone');
  const cardMoney = document.getElementById('cardMoney');
  const cardUssd = document.getElementById('cardUssd');

  cardUrl.className = hasUrl ? 'h-card threat' : 'h-card';
  document.getElementById('valUrl').textContent = hasUrl ? '[PERINGATAN] Tautan Terdeteksi' : '[OK] Bebas Tautan';

  cardPhone.className = hasPhone ? 'h-card threat' : 'h-card';
  document.getElementById('valPhone').textContent = hasPhone 
    ? (lang === 'en' ? '[ALERT] Premium/UK Number Found' : '[PERINGATAN] Kontak Pribadi Ada') 
    : '[OK] Bebas Kontak Pribadi';

  cardMoney.className = hasMoney ? 'h-card threat' : 'h-card';
  document.getElementById('valMoney').textContent = hasMoney 
    ? (lang === 'en' ? '[ALERT] Currency Mentioned (£/$)' : '[PERINGATAN] Klaim Uang Ada') 
    : '[OK] Tidak Disebutkan';

  cardUssd.className = hasUssd ? 'h-card threat' : 'h-card';
  document.getElementById('valUssd').textContent = hasUssd ? '[INFO] Kode USSD Terdeteksi' : '[OK] Tidak Ada';

  const langTag = lang === 'en' ? ' [ENGLISH MODEL]' : ' [INDONESIAN MODEL]';

  if (verdict === "PENIPUAN") {
    resultDisplay.classList.add('scam');
    resultVerdict.textContent = `PERINGATAN: SMS PENIPUAN (SMISHING)${langTag}`;
    resultSub.textContent = lang === 'en'
      ? "Pesan berbahasa Inggris ini terindikasi kuat sebagai International Smishing, pencurian identitas, atau penipuan pulsa tarif premium."
      : "Pesan ini terindikasi kuat sebagai kejahatan siber rekayasa sosial atau tautan berbahaya.";
    scoreBadge.textContent = `${scamPct}% PENIPUAN`;

    adviceTitle.textContent = "PANDUAN KEAMANAN SIBER SEGERA:";
    if (lang === 'en') {
      if (lower.includes('0906') || lower.includes('call')) {
        adviceText.textContent = "JANGAN MENELEPON nomor telepon yang tertera (0906 / premium rate). Nomor ini merupakan penipuan panggilan premium bertarif tinggi (£1.50 - £3/menit) yang dirancang untuk menguras pulsa atau tagihan telepon Anda.";
      } else if (hasUrl) {
        adviceText.textContent = "JANGAN KLIK tautan web yang dicantumkan. Tautan tersebut mengarah ke situs tiruan (phishing website) PayPal, Royal Mail, atau perbankan internasional untuk mencuri password dan data kartu kredit.";
      } else {
        adviceText.textContent = "JANGAN BALAS pesan ini. Ini adalah skema penipuan hadiah palsu (lottery fraud) atau phishing akun. Segera hapus pesan ini dari ponsel Anda.";
      }
    } else {
      if (lower.includes('.apk')) {
        adviceText.textContent = "JANGAN PERNAH mengunduh atau menginstal file berekstensi .APK tersebut. File ini adalah malware SMS-Sniffer yang dirancang untuk mencuri kode OTP perbankan dan membobol rekening Anda.";
      } else if (hasUrl) {
        adviceText.textContent = "JANGAN KLIK tautan web yang dicantumkan. Lembaga resmi (Shopee, Bank, Kominfo) tidak pernah membagikan tautan menggunakan shortlink bit.ly atau domain asing.";
      } else {
        adviceText.textContent = "JANGAN hubungi nomor telepon atau WhatsApp yang tertera. Jangan pernah mengirimkan uang muka, data KTP, atau kode OTP kepada pihak yang tidak dikenal.";
      }
    }
  } else if (verdict === "PROMOSI") {
    resultDisplay.classList.add('promo');
    resultVerdict.textContent = `STATUS: SMS PROMOSI / PENAWARAN (SPAM)${langTag}`;
    resultSub.textContent = lang === 'en'
      ? "Pesan berisi kampanye pemasaran resmi operator seluler atau promosi paket data internasional."
      : "Pesan berisi penawaran komersial kuota, diskon, atau buletin resmi operator.";
    scoreBadge.textContent = `${promoPct}% PROMOSI`;

    adviceTitle.textContent = "PETUNJUK TINDAKAN PENGGUNA:";
    adviceText.textContent = lang === 'en'
      ? "Pesan ini merupakan iklan komersial telekomunikasi. Jika Anda tidak berminat, abaikan pesan ini atau kirimkan perintah opt-out (misal: STOP) sesuai ketentuan."
      : "Pesan ini teridentifikasi sebagai iklan promosi layanan. Abaikan pesan ini jika tidak berminat atau bertransaksilah hanya melalui aplikasi resmi operator.";
  } else {
    resultDisplay.classList.add('safe');
    resultVerdict.textContent = `STATUS: SMS AMAN (PESAN NORMAL)${langTag}`;
    resultSub.textContent = lang === 'en'
      ? "Pesan percakapan personal santai berbahasa Inggris tanpa indikasi tautan phishing atau penipuan."
      : "Tidak ditemukan indikator ancaman rekayasa sosial atau tautan berbahaya.";
    scoreBadge.textContent = `${safePct}% AMAN`;

    adviceTitle.textContent = "STATUS PESAN: AMAN DIKONSUMSI";
    adviceText.textContent = lang === 'en'
      ? "Pesan ini terverifikasi aman. Menggunakan kosakata percakapan personal biasa tanpa pola manipulasi urgensi finansial atau pencurian data."
      : "Pesan ini memiliki pola bahasa percakapan personal biasa tanpa indikasi tautan berbahaya, peretasan, atau desakan finansial penipuan.";
  }
}

// 6. Streamlit Iframe Auto-Height & Smooth Anchor Navigation
(function () {
  try {
    const frame = window.frameElement;
    if (!frame) return;
    const fit = () => {
      frame.style.height = document.documentElement.scrollHeight + 'px';
    };
    new ResizeObserver(fit).observe(document.body);
    fit();
    document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      const target = id.length > 1 && document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  } catch (err) {
    /* abaikan */
  }
})();
