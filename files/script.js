// ==============================================================================
// SMISHINGGUARD JAVASCRIPT ENGINE (SOLID COLOR, NO EMOJIS)
// Menu, Carousel, Tabs, Presets, and Hybrid AI Detection Simulator
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

// 4. Preset Cases Data (Strictly No Emojis)
const PRESETS = {
  shopee: "Surat Keputusan Resmi Shopee 77: No. Anda terpilih pemenang Hadiah Cek Rp 175.000.000. Kode PIN: 254F77. Klaim hadiah segera hubungi WhatsApp di wa.me/6281298765432",
  apk: "Paket J&T Express tertahan di gudang drop point karena alamat kurang detail. Silakan unduh dan cek bukti foto paket Anda di: https://bit.ly/resi-paket-jnt.apk",
  pinjol: "KTA Dana Kilat: Dapatkan pinjaman tunai tanpa agunan s.d Rp 50.000.000, bunga 0%, cair 5 menit langsung ke rekening Anda. Info klik https://pinjol-kilat.id/acc atau WA 085712345678",
  promo: "Paket Flash Spesial! Nikmati Kuota 25GB berlaku 30 hari hanya Rp 50.000. Aktifkan sekarang di *363*88# atau kunjungi aplikasi MyTelkomsel. S&K berlaku.",
  normal: "Bro, besok pagi jam 9 kumpul di perpustakaan kampus ya buat selesaikan tugas akhir Machine Learning bareng kelompok."
};

const smsInput = document.getElementById('smsInput');
const charCount = document.getElementById('charCount');
const detectedLang = document.getElementById('detectedLang');
const scanBtn = document.getElementById('scanBtn');
const clearBtn = document.getElementById('clearBtn');
const resultDisplay = document.getElementById('resultDisplay');

// Update Character Counter & Detect Language
function updateTextMeta() {
  const text = smsInput.value;
  charCount.textContent = `${text.length} karakter`;

  if (text.trim().length === 0) {
    detectedLang.textContent = "AUTO (INDONESIA)";
    return;
  }

  const enWords = ['the', 'is', 'at', 'which', 'on', 'for', 'you', 'your', 'free', 'win', 'urgent', 'claim'];
  const idWords = ['yang', 'di', 'dari', 'ini', 'untuk', 'ke', 'bisa', 'anda', 'selamat', 'hadiah', 'rekening'];

  const lower = text.toLowerCase();
  let enCount = 0;
  let idCount = 0;

  enWords.forEach(w => { if (new RegExp('\\b' + w + '\\b').test(lower)) enCount++; });
  idWords.forEach(w => { if (new RegExp('\\b' + w + '\\b').test(lower)) idCount++; });

  if (enCount > idCount) {
    detectedLang.textContent = "BAHASA INGGRIS (EN)";
  } else {
    detectedLang.textContent = "BAHASA INDONESIA (ID)";
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
// 5. HYBRID AI & HEURISTIC ENGINE (Real-Time In-Browser Inference)
// ==============================================================================
function runSmishingAnalysis(text) {
  const lower = text.toLowerCase();

  const urlRegex = /(https?:\/\/[^\s]+|bit\.ly\/[^\s]+|wa\.me\/[^\s]+|tinyurl\.com\/[^\s]+|s\.id\/[^\s]+|[a-z0-9-]+\.(?:xyz|top|info|site|club|vip|online|app|icu|cyou|live|me|com|id|net)[^\s]*)/i;
  const phoneRegex = /(?:\+?62|08)[0-9]{8,12}\b/;
  const moneyRegex = /(?:rp\.?\s*[\d\.,]+|\b\d+\s*(?:juta|jt|ribu|rb|miliar|m|usd|dolar)\b|\$[\d\.,]+)/i;
  const ussdRegex = /\*[0-9]+(?:\*[0-9]+)*#/;

  const hasUrl = urlRegex.test(text);
  const hasPhone = phoneRegex.test(text);
  const hasMoney = moneyRegex.test(text);
  const hasUssd = ussdRegex.test(text);

  const scamKeywords = [
    'undian', 'hadiah', 'shopee', 'pinjaman', 'dana kilat', 'tanpa agunan', 'cek', 'pemenang',
    'surat keputusan', 'rekening', 'diblokir', 'verifikasi akun', 'apk', 'paket tertahan',
    'bunga 0%', 'cair', 'klaim', 'pin', 'bca', 'bri', 'mandiri', 'link', 'klik'
  ];

  const promoKeywords = [
    'promo', 'kuota', 'gb', 'paket', 'flash', 'diskon', 'telkomsel', 'indosat', 'xl',
    'berlaku', 'aktifkan', 'mytelkomsel', 'tarif', 'cashback', 'voucher'
  ];

  let scamScore = 0;
  scamKeywords.forEach(k => {
    if (lower.includes(k)) scamScore += 1.5;
  });
  if (hasUrl) scamScore += 3;
  if (hasPhone) scamScore += 2;
  if (hasMoney) scamScore += 2.5;
  if (lower.includes('.apk')) scamScore += 5;

  let promoScore = 0;
  promoKeywords.forEach(k => {
    if (lower.includes(k)) promoScore += 1.5;
  });
  if (hasUssd) promoScore += 4;

  let verdict = "NORMAL";
  let pScam = 0.01;
  let pSafe = 0.98;
  let pPromo = 0.01;

  if (scamScore >= 4 || lower.includes('.apk') || (hasUrl && hasMoney) || (hasPhone && lower.includes('selamat'))) {
    verdict = "PENIPUAN";
    pScam = Math.min(0.99, 0.85 + (scamScore * 0.02));
    pSafe = Math.max(0.005, (1 - pScam) * 0.4);
    pPromo = 1 - pScam - pSafe;
  } else if (promoScore >= 3 || (hasUssd && lower.includes('kuota'))) {
    verdict = "PROMOSI";
    pPromo = Math.min(0.98, 0.80 + (promoScore * 0.03));
    pSafe = Math.max(0.01, (1 - pPromo) * 0.6);
    pScam = 1 - pPromo - pSafe;
  } else {
    verdict = "NORMAL";
    pSafe = 0.985;
    pScam = 0.009;
    pPromo = 0.006;
  }

  displayResults(verdict, pScam, pSafe, pPromo, hasUrl, hasPhone, hasMoney, hasUssd, lower);
}

function displayResults(verdict, pScam, pSafe, pPromo, hasUrl, hasPhone, hasMoney, hasUssd, lower) {
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
  document.getElementById('valPhone').textContent = hasPhone ? '[PERINGATAN] Kontak Pribadi Ada' : '[OK] Bebas Kontak Pribadi';

  cardMoney.className = hasMoney ? 'h-card threat' : 'h-card';
  document.getElementById('valMoney').textContent = hasMoney ? '[PERINGATAN] Klaim Uang Ada' : '[OK] Tidak Disebutkan';

  cardUssd.className = hasUssd ? 'h-card threat' : 'h-card';
  document.getElementById('valUssd').textContent = hasUssd ? '[INFO] Kode USSD Terdeteksi' : '[OK] Tidak Ada';

  if (verdict === "PENIPUAN") {
    resultDisplay.classList.add('scam');
    resultVerdict.textContent = "PERINGATAN: SMS PENIPUAN (SMISHING)";
    resultSub.textContent = "Pesan ini terindikasi kuat sebagai kejahatan siber rekayasa sosial atau tautan berbahaya.";
    scoreBadge.textContent = `${scamPct}% PENIPUAN`;

    adviceTitle.textContent = "PANDUAN KEAMANAN SIBER SEGERA:";
    if (lower.includes('.apk')) {
      adviceText.textContent = "JANGAN PERNAH mengunduh atau menginstal file berekstensi .APK tersebut. File ini adalah malware SMS-Sniffer yang dirancang untuk mencuri kode OTP perbankan dan membobol rekening Anda.";
    } else if (hasUrl) {
      adviceText.textContent = "JANGAN KLIK tautan web yang dicantumkan. Lembaga resmi (Shopee, Bank, Kominfo) tidak pernah membagikan tautan menggunakan shortlink bit.ly atau domain asing.";
    } else {
      adviceText.textContent = "JANGAN hubungi nomor telepon atau WhatsApp yang tertera. Jangan pernah mengirimkan uang muka, data KTP, atau kode OTP kepada pihak yang tidak dikenal.";
    }
  } else if (verdict === "PROMOSI") {
    resultDisplay.classList.add('promo');
    resultVerdict.textContent = "STATUS: SMS PROMOSI / PENAWARAN (SPAM)";
    resultSub.textContent = "Pesan berisi penawaran komersial kuota, diskon, atau buletin resmi operator.";
    scoreBadge.textContent = `${promoPct}% PROMOSI`;

    adviceTitle.textContent = "PETUNJUK TINDAKAN PENGGUNA:";
    adviceText.textContent = "Pesan ini teridentifikasi sebagai iklan promosi layanan. Abaikan pesan ini jika tidak berminat atau bertransaksilah hanya melalui aplikasi resmi operator.";
  } else {
    resultDisplay.classList.add('safe');
    resultVerdict.textContent = "STATUS: SMS AMAN (PESAN NORMAL)";
    resultSub.textContent = "Tidak ditemukan indikator ancaman rekayasa sosial atau tautan berbahaya.";
    scoreBadge.textContent = `${safePct}% AMAN`;

    adviceTitle.textContent = "STATUS PESAN: AMAN DIKONSUMSI";
    adviceText.textContent = "Pesan ini memiliki pola bahasa percakapan personal biasa tanpa indikasi tautan berbahaya, peretasan, atau desakan finansial penipuan.";
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
