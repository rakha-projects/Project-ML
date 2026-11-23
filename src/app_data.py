"""Validated app resources and in-memory CSV input."""
from __future__ import annotations
import hashlib
import csv
import io
import json
from pathlib import Path
import joblib
import pandas as pd
import sklearn

ROOT = Path(__file__).resolve().parents[1]
MAX_CSV_BYTES = 2 * 1024 * 1024
MAX_CSV_ROWS = 1000


def load_resources():
    evaluation = json.loads((ROOT / 'models/evaluation.json').read_text(encoding='utf-8'))
    if evaluation.get('schema_version') != 3:
        raise ValueError('Artefak belum selaras. Jalankan python -m src.train lalu python -m src.evaluate.')
    if evaluation['scikit_learn_version'] != sklearn.__version__:
        raise ValueError('Versi scikit-learn berbeda dari artefak. Instal requirements.txt atau latih ulang model.')
    for name, expected in evaluation['artifact_sha256'].items():
        if hashlib.sha256((ROOT / 'models' / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Artefak model berubah. Jalankan kembali python -m src.train dan python -m src.evaluate.')
    source = ROOT / 'src/preprocessing.py'
    if hashlib.sha256(source.read_text(encoding='utf-8-sig').encode('utf-8')).hexdigest() != evaluation['source_sha256']['preprocessing_py']:
        raise ValueError('Preprocessing berubah sejak training. Latih ulang model sebelum menjalankan aplikasi.')
    pipelines = {lang: joblib.load(ROOT / f'models/best_model_{lang}.joblib') for lang in ('id', 'en')}
    if any(not hasattr(model, 'named_steps') for model in pipelines.values()):
        raise ValueError('Format model tidak kompatibel. Jalankan python -m src.train.')
    return pipelines, evaluation


def parse_csv(data: bytes, separator: str = 'Otomatis', encoding: str = 'Otomatis') -> pd.DataFrame:
    if len(data) > MAX_CSV_BYTES:
        raise ValueError('Ukuran CSV melebihi 2 MB.')
    if not data or not data.strip():
        raise ValueError('Berkas CSV kosong.')
    text = None
    for codec in (['utf-8-sig', 'cp1252'] if encoding == 'Otomatis' else [encoding]):
        try:
            text = data.decode(codec)
            break
        except UnicodeDecodeError:
            pass
    if text is None:
        raise ValueError('Encoding CSV tidak terbaca. Pilih UTF-8 atau Windows-1252.')
    if '\x00' in text:
        raise ValueError('Berkas tidak terbaca sebagai CSV teks. Ekspor ulang sebagai CSV UTF-8.')
    if separator == 'Otomatis':
        try:
            delimiter = csv.Sniffer().sniff(text[:8192], delimiters=',;\t|').delimiter
        except csv.Error:
            delimiter = ','  # A CSV containing just one SMS column has no separator.
    else:
        delimiter = separator
    try:
        frame = pd.read_csv(io.StringIO(text), sep=delimiter,
                            engine='python', dtype=str, keep_default_na=False,
                            nrows=MAX_CSV_ROWS + 1, skip_blank_lines=False)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError, csv.Error) as exc:
        raise ValueError('Format CSV tidak terbaca. Periksa pemisah dan tanda kutip pada setiap baris.') from exc
    if frame.empty:
        raise ValueError('CSV hanya berisi header atau tidak memiliki baris SMS.')
    if len(frame) > MAX_CSV_ROWS:
        raise ValueError('CSV melebihi 1.000 baris. Bagi berkas menjadi beberapa bagian.')
    return frame.fillna('')
