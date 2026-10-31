"""
Skrip Standardisasi & Penyeragaman Format Dataset (Indonesia & Inggris).
Menghasilkan format kolom yang seragam 100% untuk kedua bahasa.
"""

import os
import glob
import json
import csv
from collections import Counter
from preprocessing import clean_text, extract_heuristic_features, detect_language

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDO_INPUT = os.path.join(BASE_DIR, "Indonesia", "dataset_clean.csv")
ENG_GLOB = os.path.join(BASE_DIR, "Inggris", "*.jsonl")

INDO_OUTPUT = os.path.join(BASE_DIR, "Indonesia", "dataset_indonesia_standard.csv")
ENG_OUTPUT = os.path.join(BASE_DIR, "Inggris", "dataset_inggris_standard.csv")
MULTILINGUAL_BALANCED = os.path.join(BASE_DIR, "dataset_multilingual_balanced.csv")

STANDARD_FIELDS = [
    "text",
    "cleaned_text",
    "language",
    "label_3class",
    "label_2class",
    "label_name",
    "sub_category",
    "text_length",
    "word_count",
    "has_url",
    "has_phone",
    "has_nominal",
    "has_shortcode",
    "heuristic_risk_score"
]

def process_indonesia():
    print(f"\n[*] Memproses dataset Indonesia dari: {INDO_INPUT}")
    rows = []
    with open(INDO_INPUT, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for r in reader:
            lbl = int(r["label"])
            # Mapping 3-class & 2-class
            # 0 = Normal, 1 = Penipuan, 2 = Promosi
            # Untuk 2-class: 0 = Normal, 1 = Phishing/Spam (Penipuan & Promosi)
            lbl_2class = 0 if lbl == 0 else 1
            lbl_name = r["label_name"]
            
            rows.append({
                "text": r["original_text"],
                "cleaned_text": r["cleaned_text"],
                "language": "id",
                "label_3class": lbl,
                "label_2class": lbl_2class,
                "label_name": lbl_name,
                "sub_category": lbl_name.lower(),
                "text_length": int(r["text_length"]),
                "word_count": int(r["word_count"]),
                "has_url": int(r["has_url"]),
                "has_phone": int(r["has_phone"]),
                "has_nominal": int(r["has_nominal"]),
                "has_shortcode": int(r["has_shortcode"]),
                "heuristic_risk_score": int(r["heuristic_risk_score"])
            })

    print(f"[+] Berhasil memproses {len(rows)} data Indonesia.")
    return rows


def process_english(sample_limit_per_category: int = 5000):
    """
    Memproses dataset Inggris dari 60 file JSONL.
    Menyelaraskan kategori ke skema standar yang identik dengan Indonesia.
    """
    files = sorted(glob.glob(ENG_GLOB))
    print(f"\n[*] Memproses dataset Inggris dari {len(files)} file JSONL...")

    category_counts = Counter()
    rows = []

    # Mapping kategori Inggris ke 3-Class
    # 0 = Normal, 1 = Penipuan, 2 = Promosi
    fraud_cats = {"phishing", "crypto", "job_scam", "giveaway", "scam", "adult"}
    promo_cats = {"marketing", "promo"}

    for fpath in files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                cat = str(data.get("category", "spam")).lower()
                text = str(data.get("text", "")).strip()
                if not text:
                    continue

                # Pembatasan proporsional agar data seimbang dan cepat diolah
                if category_counts[cat] >= sample_limit_per_category:
                    continue

                category_counts[cat] += 1

                # Tentukan label 3-class & 2-class
                if cat == "normal":
                    lbl_3 = 0
                    lbl_2 = 0
                    lbl_name = "Normal"
                elif cat in fraud_cats:
                    lbl_3 = 1
                    lbl_2 = 1
                    lbl_name = "Penipuan"
                elif cat in promo_cats:
                    lbl_3 = 2
                    lbl_2 = 1
                    lbl_name = "Promosi"
                else:  # 'spam' umum
                    # Deteksi apakah condong ke promosi atau penipuan
                    text_lower = text.lower()
                    if any(w in text_lower for w in ["sale", "offer", "discount", "order", "delivery", "shop"]):
                        lbl_3 = 2
                        lbl_2 = 1
                        lbl_name = "Promosi"
                    else:
                        lbl_3 = 1
                        lbl_2 = 1
                        lbl_name = "Penipuan"

                cleaned = clean_text(text, lang="en")
                heuristics = extract_heuristic_features(text, lang="en")

                rows.append({
                    "text": text,
                    "cleaned_text": cleaned,
                    "language": "en",
                    "label_3class": lbl_3,
                    "label_2class": lbl_2,
                    "label_name": lbl_name,
                    "sub_category": cat,
                    "text_length": heuristics["text_length"],
                    "word_count": heuristics["word_count"],
                    "has_url": int(heuristics["has_url"]),
                    "has_phone": int(heuristics["has_phone"]),
                    "has_nominal": int(heuristics["has_nominal"]),
                    "has_shortcode": int(heuristics["has_shortcode"]),
                    "heuristic_risk_score": heuristics["heuristic_risk_score"]
                })

    print(f"[+] Berhasil memproses {len(rows)} data Inggris.")
    print("    Distribusi kategori asal:", dict(category_counts))
    return rows


def save_csv(filepath: str, data: list):
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=STANDARD_FIELDS)
        writer.writeheader()
        writer.writerows(data)
    print(f"[V] Tersimpan di: {filepath} ({len(data)} baris)")


def main():
    print("=" * 70)
    print("PENYELARASAN DATASET INGGRIS & INDONESIA KE STANDAR TUNGGAL")
    print("=" * 70)

    indo_data = process_indonesia()
    eng_data = process_english(sample_limit_per_category=3000)

    # 1. Simpan dataset Indonesia standar
    save_csv(INDO_OUTPUT, indo_data)

    # 2. Simpan dataset Inggris standar
    save_csv(ENG_OUTPUT, eng_data)

    # 3. Buat dataset Multilingual Balanced (Dwibahasa Seimbang)
    # Ambil proporsi seimbang antara Indo (1.138) dan subset Inggris terpilih (~1.500)
    import random
    random.seed(42)
    eng_sample = random.sample(eng_data, min(1500, len(eng_data)))
    multilingual = indo_data + eng_sample
    random.shuffle(multilingual)
    save_csv(MULTILINGUAL_BALANCED, multilingual)

    print("\n" + "=" * 70)
    print("RINGKASAN HASIL PENYELARASAN DATASET:")
    print(f"1. Indonesia Standard    : {len(indo_data)} baris -> {INDO_OUTPUT}")
    print(f"2. Inggris Standard      : {len(eng_data)} baris -> {ENG_OUTPUT}")
    print(f"3. Multilingual Balanced : {len(multilingual)} baris -> {MULTILINGUAL_BALANCED}")
    print("Format kolom kedua dataset kini 100% IDENTIK dan siap dilatih!")
    print("=" * 70)

if __name__ == "__main__":
    main()

