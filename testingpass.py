import unittest
from sampledata_enhanced import load_fitness_data, compute_avg_steps, sleep_score
import pandas as pd
import io

class TestFitnessAnalysis(unittest.TestCase):

    def setUp(self):
        self.valid_csv = """timestamp,steps,heart_rate,sleep_duration
2026-01-01 08:00:00,8500,72,7.5
2026-01-02 08:00:00,9200,75,8.0"""

    def test_load_valid_data(self):
        """PASS: Loads valid data successfully."""
        df = load_fitness_data(self.valid_csv)
        self.assertEqual(len(df), 2)
        self.assertAlmostEqual(df['steps'].mean(), 8850)

    def test_load_negative_steps(self):
        """FAIL: Raises error for negative steps."""
        invalid_csv = self.valid_csv + "\n2026-01-03 08:00:00,-100,70,8.0"
        with self.assertRaises(ValueError):
            load_fitness_data(invalid_csv)

    def test_compute_avg_steps_valid(self):
        """PASS: Computes average steps correctly."""
        df = pd.DataFrame({'steps': [8500, 9200]})
        avg = compute_avg_steps(df)
        self.assertAlmostEqual(avg, 8850)

    def test_sleep_score_optimal(self):
        """PASS: Optimal sleep score."""
        self.assertEqual(sleep_score(8.0), 1.0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
