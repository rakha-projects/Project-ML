"""Checks for the prediction path used by both app views."""

import unittest
from pathlib import Path

import joblib
import pandas as pd

from src.inference import MAX_SMS_CHARS, analyze_batch, analyze_sms, safe_csv_bytes


ROOT = Path(__file__).resolve().parents[1]


class InferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipelines = {
            "id": joblib.load(ROOT / "models" / "best_model_id.joblib"),
            "en": joblib.load(ROOT / "models" / "best_model_en.joblib"),
        }

    def test_single_message_routes_to_manual_language(self):
        result = analyze_sms("Besok kuliah jam delapan pagi di lab", "id", self.pipelines)
        self.assertEqual(result["language"], "id")
        self.assertIn(result["label"], {"Normal", "Penipuan", "Promosi"})
        self.assertAlmostEqual(sum(result["probabilities"].values()), 1.0, places=5)

    def test_empty_and_long_message_rejected(self):
        with self.assertRaises(ValueError):
            analyze_sms("  ", "auto", self.pipelines)
        with self.assertRaises(ValueError):
            analyze_sms("a" * (MAX_SMS_CHARS + 1), "id", self.pipelines)

    def test_batch_marks_empty_rows_and_uses_selected_language(self):
        frame = pd.DataFrame({"sms": ["Besok kuliah jam delapan", None]})
        result = analyze_batch(frame, "sms", "id", self.pipelines)
        self.assertEqual(result.loc[0, "Bahasa_Model"], "id")
        self.assertIn("Status_Risiko", result.columns)
        self.assertTrue(0 <= result.loc[0, "Keyakinan_Model_%"] <= 100)
        self.assertEqual(result.loc[1, "Prediksi_Kategori"], "")
        self.assertIn("kosong", result.loc[1, "Status"])

    def test_csv_export_escapes_formulas(self):
        frame = pd.DataFrame({"sms": ["=HYPERLINK(\"https://example.test\")"]})
        self.assertIn("'=HYPERLINK", safe_csv_bytes(frame).decode("utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
