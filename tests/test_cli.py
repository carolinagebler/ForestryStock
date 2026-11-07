"""Command-line behavior."""

import contextlib
import io
import json
import unittest
from pathlib import Path

from forestrystock.cli import main

DATA = Path(__file__).resolve().parents[1] / "data"


class CommandTests(unittest.TestCase):
    def test_summary_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["summary", "--data", str(DATA)])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue())["stand_count"], 240)

    def test_bad_path_has_exit_code(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            status = main(["summary", "--data", "/missing/data/directory"])
        self.assertEqual(status, 2)
        self.assertIn("Cannot read", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
