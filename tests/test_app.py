"""CSV validation and end-to-end Streamlit interaction checks."""
import io
import unittest
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from src.app_data import MAX_CSV_BYTES, MAX_CSV_ROWS, ROOT, load_resources, parse_csv
from src.inference import MAX_SMS_CHARS, analyze_batch, analyze_sms, safe_csv_bytes


class CsvTests(unittest.TestCase):
    def test_single_column_example_is_not_split_on_letters(self):
        frame = parse_csv((ROOT / 'laporan/contoh_sms.csv').read_bytes())
        self.assertEqual(list(frame.columns), ['sms'])
        self.assertEqual(len(frame), 4)

    def test_semicolon_tab_and_windows_encoding(self):
        for delimiter in (';', '\t'):
            frame = parse_csv(f'id{delimiter}pesan\n1{delimiter}Besok kuliah\n'.encode())
            self.assertEqual(frame.loc[0, 'pesan'], 'Besok kuliah')
        frame = parse_csv('sms\n"Claim £100 now"\n'.encode('cp1252'))
        self.assertIn('£100', frame.loc[0, 'sms'])

    def test_blank_rows_are_preserved_for_validation(self):
        frame = parse_csv(b'id;sms\n1;Besok kuliah\n2;\n')
        self.assertEqual(frame.loc[1, 'sms'], '')

    def test_reject_invalid_empty_and_oversized_files(self):
        for content in (b'', b'sms\n', b'\x00binary', b'a' * (MAX_CSV_BYTES + 1),
                        b'sms\n"unterminated', ('sms\n' + 'teks\n' * (MAX_CSV_ROWS + 1)).encode()):
            with self.subTest(content=content[:20]), self.assertRaises(ValueError):
                parse_csv(content)

    def test_accept_maximum_rows(self):
        frame = parse_csv(('sms\n' + 'Besok kuliah\n' * MAX_CSV_ROWS).encode())
        self.assertEqual(len(frame), MAX_CSV_ROWS)

    def test_preserve_uploaded_result_column(self):
        pipelines, _ = load_resources()
        frame = pd.DataFrame({'sms': ['Besok kuliah pagi'], 'Status': ['Asli'], 'Status_Input': ['Arsip']})
        result = analyze_batch(frame, 'sms', 'id', pipelines)
        self.assertEqual(result.loc[0, 'Status_Input_Input'], 'Asli')
        self.assertEqual(result.loc[0, 'Status_Input'], 'Arsip')
        self.assertEqual(frame.loc[0, 'Status'], 'Asli')

    def test_header_and_cells_are_safe_for_export(self):
        data = safe_csv_bytes(pd.DataFrame({'=formula': ['\t=HYPERLINK("x")', '+SUM(1)', 'Normal']}))
        result = pd.read_csv(io.BytesIO(data))
        self.assertEqual(result.columns[0], "'=formula")
        self.assertTrue(result.iloc[0, 0].startswith("'"))
        self.assertEqual(result.iloc[2, 0], 'Normal')


class StreamlitTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        self.assertFalse(self.app.exception)

    def test_four_modules_load_and_empty_input_shows_error(self):
        self.assertEqual(len(self.app.tabs), 4)
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertIn('kosong', self.app.error[0].value)

    def test_presets_use_real_model_for_both_languages(self):
        for collection, lang in (('Indonesia', 'id'), ('English', 'en')):
            self.app.selectbox(key='example_language').select(collection).run()
            for category in ('Normal', 'Penipuan', 'Promosi'):
                self.app.button(key=f'preset_{category}').click().run(timeout=30)
                self.assertFalse(self.app.exception)
                saved = self.app.session_state['single_result']
                self.assertEqual(saved['result']['language'], lang)
                expected = analyze_sms(saved['text'], lang, load_resources()[0])
                self.assertEqual(saved['result']['probabilities'], expected['probabilities'])
                self.assertTrue(saved['result']['contributions'])

    def test_changed_input_hides_old_result_and_clear_resets(self):
        self.app.button(key='preset_Penipuan').click().run()
        self.app.text_area(key='sms_text').input('Besok kuliah jam delapan').run()
        # User sees the stale-result prompt, not the old verdict.
        markup = ' '.join(element.proto.body for element in self.app.get('html'))
        self.assertIn('Pesan telah berubah', markup)
        self.assertNotIn('Prediksi kategori pesan', markup)
        self.app.button[1].click().run()
        self.assertEqual(self.app.text_area(key='sms_text').value, '')
        self.assertNotIn('single_result', self.app.session_state)

    def test_each_model_confusion_matrix_and_eda_view_render(self):
        for model in ('Multinomial Naive Bayes', 'Logistic Regression', 'Linear SVM'):
            widget = next(item for item in self.app.selectbox if item.label == 'Tinjau hasil algoritma')
            widget.select(model).run(timeout=30)
            self.assertFalse(self.app.exception)

    def test_batch_upload_process_and_download(self):
        class Uploaded(io.BytesIO):
            name = 'test.csv'
        file = Uploaded(b'id;sms\n1;Besok kuliah jam delapan\n2;\n')
        with patch('streamlit.file_uploader', return_value=file):
            self.app.run(timeout=30)
            button = next(item for item in self.app.button if item.label == 'Proses semua pesan')
            button.click().run(timeout=30)
            self.assertFalse(self.app.exception)
            output = self.app.session_state['batch_result']['output']
            self.assertEqual(len(output), 2)
            self.assertEqual(output.loc[0, 'Status'], 'Terproses')
            self.assertIn('kosong', output.loc[1, 'Status'])
            widget = next(item for item in self.app.selectbox if item.label == 'Filter tabel hasil')
            widget.select('Tidak valid').run(timeout=30)
            self.assertFalse(self.app.exception)
            self.assertTrue(any(item.label == 'Unduh seluruh hasil CSV' for item in self.app.get('download_button')))


if __name__ == '__main__':
    unittest.main()
