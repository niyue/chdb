import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

import chdb


class TestProgressModes(unittest.TestCase):
    def run_query_with_progress(self, mode):
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                res = chdb.query("SELECT 1", progress=mode)
        except TypeError:
            self.skipTest("progress parameter not supported in this build")
        return res.bytes(), buf_out.getvalue(), buf_err.getvalue()

    def test_progress_none(self):
        data, out, err = self.run_query_with_progress("none")
        self.assertEqual(data, b"1\n")
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_progress_bar(self):
        data, out, err = self.run_query_with_progress("bar")
        self.assertEqual(data, b"1\n")
        # Progress bar prints to stderr when attached to a TTY; we should see no stdout noise.
        self.assertEqual(out, "")
        self.assertIsInstance(err, str)

    def test_progress_table(self):
        data, out, err = self.run_query_with_progress("table")
        self.assertEqual(data, b"1\n")
        # Progress table writes to stderr; stdout should stay clean.
        self.assertEqual(out, "")
        self.assertIsInstance(err, str)


if __name__ == "__main__":
    unittest.main()
