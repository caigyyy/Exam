import unittest
import pandas as pd
import io
from sampledata.py import load_data  # Assume refactored into function

class TestDataIngestion(unittest.TestCase):
    def test_valid_data(self):
        csv_valid = "timestamp,steps,heartrate,sleepduration\n2026-01-01,8500,72,7.5"
        df = load_data(csv_valid)
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 1)

    def test_empty_data(self):
        df = load_data("")
        self.assertTrue(df.empty)

    def test_corrupt_data(self):
        with self.assertRaises(pd.errors.ParserError):
            load_data("invalid,notcsv")

    def test_negative_steps(self):
        csv_neg = "timestamp,steps,heartrate,sleepduration\n2026-01-01,-100,72,7.5"
        with self.assertRaises(ValueError):
            load_data(csv_neg)
