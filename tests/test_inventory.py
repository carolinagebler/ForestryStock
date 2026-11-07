"""Checks for stand and harvest-area summaries."""

import csv
import tempfile
import unittest
from pathlib import Path

from forestrystock.data import DataError, nonnegative_float, read_table
from forestrystock.inventory import portfolio_summary, harvest_area_summary, load_stands

DATA = Path(__file__).resolve().parents[1] / "data"


class InventoryTests(unittest.TestCase):
    def test_summary_for_supplied_records(self):
        summary = portfolio_summary(DATA)
        self.assertEqual(summary["stand_count"], 240)
        self.assertGreater(summary["total_area_ha"], 100000)

    def test_harvest_areas_for_supplied_records(self):
        summary = harvest_area_summary(DATA)
        self.assertGreater(summary["event_count"], 0)
        self.assertGreater(summary["executed_area_ha"], 0)

    def test_numeric_field_rejects_nonfinite(self):
        for number in ("nan", "inf", "-4", "nope"):
            with self.subTest(number=number), self.assertRaises(DataError):
                nonnegative_float(number, "test")

    def test_bad_column_set_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "stands.csv").write_text("stand_id,region\nT001,north\n")
            with self.assertRaisesRegex(DataError, "missing columns"):
                read_table(d, "stands.csv")

    def test_duplicate_stand_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with (Path(d) / "stands.csv").open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["stand_id", "management_unit", "region", "land_area_ha"])
                writer.writeheader()
                for _ in range(2):
                    writer.writerow({"stand_id": "T001", "management_unit": "MU-01", "region": "North", "land_area_ha": "10"})
            with self.assertRaisesRegex(DataError, "duplicate stand"):
                load_stands(d)


if __name__ == "__main__":
    unittest.main()
