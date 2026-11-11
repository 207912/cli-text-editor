import re
import subprocess
import sys
import unittest
from pathlib import Path


EDITOR = Path(__file__).resolve().parents[1] / "editor.py"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


class EditorCLITests(unittest.TestCase):
    def run_editor(self, *commands):
        result = subprocess.run(
            [sys.executable, str(EDITOR)],
            input="".join(f"{command}\n" for command in commands),
            text=True,
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_word_navigation_on_empty_lines(self):
        output = self.run_editor("b", "e", "w", "iword", "$", "o", "b", "e", "q")
        self.assertIn("word", ANSI.sub("", output))

    def test_backwards_deletion_does_not_duplicate_text(self):
        output = self.run_editor("ialpha beta gamma", "w", "db", "v", "q")
        self.assertTrue(output.endswith("> eta gamma\n> "))

    def test_word_end_after_whitespace(self):
        output = self.run_editor("iA b cc", "l", "e", "q")
        self.assertIn("A \x1b[42mb\x1b[0m cc", output)

    def test_line_movement_and_plain_view(self):
        output = self.run_editor("ifirst", "o", "isecond", "J", "v", "q")
        self.assertTrue(output.endswith("> second\nfirst\n> "))

    def test_switching_to_a_shorter_line_clamps_the_cursor(self):
        output = self.run_editor("ix", "o", "isecond", "$", "j", "x", "v", "q")
        self.assertTrue(output.endswith("> \nsecond\n> "))

    def test_line_number_validation(self):
        output = self.run_editor("²", "0", "ifirst", "o", "isecond", "1", "q")
        self.assertTrue(output.endswith("> \x1b[42mf\x1b[0mirst\nsecond\n> "))

    def test_eof_exits_cleanly(self):
        self.assertTrue(self.run_editor("ifirst").endswith("> \n"))


if __name__ == "__main__":
    unittest.main()
