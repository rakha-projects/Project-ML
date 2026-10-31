"""
Skrip Audit Dataset dan Pra-pemrosesan Awal Korpus SMS Indonesia.
Mengecek missing value, duplikasi data, konsistensi label,
dan memproduksi dataset bersih terstandarisasi.
"""

import csv
import os
import sys
from collections import Counter
from preprocessing import clean_text, extract_heuristic_features

DATASET_INPUT = os.path.join(os.path.dirname(__file__), "..", "Indonesia", "dataset_sms_spam_v1.csv")
DATASET_CLEAN_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "Indonesia", "dataset_clean.csv")

LABEL_MAPPING = {
    "0": "Normal",
    "1": "Penipuan",
    "2": "Promosi"
}

def audit_and_clean():
    print(f"[*] Membaca dataset dari: {DATASET_INPUT}")
    if not os.path.exists(DATASET_INPUT):
        print(f"[!] File {DATASET_INPUT} tidak ditemukan!")
        sys.exit(1)

    raw_rows = []
    with open(DATASET_INPUT, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
        for idx, row in enumerate(reader, start=1):
            if len(row) >= 2:
                text = row[0].strip()
                label = row[1].strip()
                raw_rows.append((text, label))
            else:
                print(f"[!] Baris {idx} tidak lengkap: {row}")

    total_raw = len(raw_rows)
    print(f"[*] Total baris data mentah: {total_raw}")

    # 1. Analisis Missing / Kosong
    valid_rows = [(t, l) for t, l in raw_rows if t and l in LABEL_MAPPING]
    missing_count = total_raw - len(valid_rows)
    print(f"[*] Baris kosong / label tidak valid: {missing_count}")

    # 2. Distribusi Label Awal
    label_counts_raw = Counter([l for _, l in valid_rows])
    print("\n--- Distribusi Label Data Awal ---")
    for k, v in sorted(label_counts_raw.items()):
        pct = (v / len(valid_rows)) * 100
        print(f"  Kelas {k} ({LABEL_MAPPING[k]:<8}): {v:>4} sampel ({pct:5.2f}%)")

    # 3. Analisis Duplikasi Teks Mentah
    text_counter = Counter([t for t, _ in valid_rows])
    duplicate_texts = {t: c for t, c in text_counter.items() if c > 1}
    print(f"\n[*] Jumlah teks mentah duplikat: {len(duplicate_texts)} teks unik (total {sum(duplicate_texts.values())} baris)")

    # 4. Pembersihan & Deduplikasi
    # Mempertahankan teks unik, jika ada perbedaan label pada teks yang sama, gunakan label mayoritas
    unique_data = {}
    for text, label in valid_rows:
        cleaned = clean_text(text)
        if not cleaned:
            continue
        if cleaned not in unique_data:
            unique_data[cleaned] = {
                "original_text": text,
                "cleaned_text": cleaned,
                "labels": [label]
            }
        else:
            unique_data[cleaned]["labels"].append(label)

    # Resolve label mayoritas
    deduplicated_rows = []
    conflict_count = 0
    for cleaned, info in unique_data.items():
        label_freq = Counter(info["labels"])
        most_common_label, count = label_freq.most_common(1)[0]
        if len(label_freq) > 1:
            conflict_count += 1
        
        # Ekstrak heuristik
        heuristics = extract_heuristic_features(info["original_text"])
        
        deduplicated_rows.append({
            "original_text": info["original_text"],
            "cleaned_text": cleaned,
            "label": most_common_label,
            "label_name": LABEL_MAPPING[most_common_label],
            "text_length": heuristics["text_length"],
            "word_count": heuristics["word_count"],
            "has_url": int(heuristics["has_url"]),
            "has_phone": int(heuristics["has_phone"]),
            "has_nominal": int(heuristics["has_nominal"]),
            "has_shortcode": int(heuristics["has_shortcode"]),
            "heuristic_risk_score": heuristics["heuristic_risk_score"]
        })

    print(f"[*] Kasus konflik label pada teks serupa: {conflict_count}")
    print(f"[*] Total data bersih setelah deduplikasi: {len(deduplicated_rows)}")

    # 5. Distribusi Label Akhir
    label_counts_final = Counter([r["label"] for r in deduplicated_rows])
    print("\n--- Distribusi Label Data Bersih (Setelah Deduplikasi) ---")
    for k, v in sorted(label_counts_final.items()):
        pct = (v / len(deduplicated_rows)) * 100
        print(f"  Kelas {k} ({LABEL_MAPPING[k]:<8}): {v:>4} sampel ({pct:5.2f}%)")

    # 6. Simpan Dataset Bersih
    output_headers = [
        "original_text", "cleaned_text", "label", "label_name",
        "text_length", "word_count", "has_url", "has_phone",
        "has_nominal", "has_shortcode", "heuristic_risk_score"
    ]
    with open(DATASET_CLEAN_OUTPUT, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output_headers)
        writer.writeheader()
        writer.writerows(deduplicated_rows)

    print(f"\n[+] Dataset bersih berhasil disimpan di: {DATASET_CLEAN_OUTPUT}")
    print("[+] Audit dataset dan pra-pemrosesan selesai dengan sukses.")

if __name__ == "__main__":
    audit_and_clean()

