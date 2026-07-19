import tempfile
import unittest
from pathlib import Path

from cd_assist.tools import FileParseError, read_file


class ReadFileTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_root = Path(self.temporary_directory.name)
        self.workspace = self.temporary_root / "workspace"
        self.workspace.mkdir()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_reads_java_file(self):
        java_file = self.workspace / "Example.java"
        java_file.write_text("public class Example {}", encoding="utf-8")

        result = read_file(self.workspace, "Example.java")

        self.assertEqual("public class Example {}", result["content"])
        self.assertFalse(result["truncated"])

    def test_accepts_uppercase_java_extension(self):
        java_file = self.workspace / "Example.JAVA"
        java_file.write_text("public class Example {}", encoding="utf-8")

        result = read_file(self.workspace, "Example.JAVA")

        self.assertEqual("public class Example {}", result["content"])

    def test_rejects_path_outside_workspace(self):
        outside_file = self.temporary_root / "Outside.java"
        outside_file.write_text("public class Outside {}", encoding="utf-8")

        with self.assertRaisesRegex(FileParseError, "outside the workspace"):
            read_file(self.workspace, "../Outside.java")

    def test_rejects_missing_file(self):
        with self.assertRaisesRegex(FileParseError, "not a file"):
            read_file(self.workspace, "Missing.java")

    def test_rejects_directory(self):
        directory = self.workspace / "Directory.java"
        directory.mkdir()

        with self.assertRaisesRegex(FileParseError, "not a file"):
            read_file(self.workspace, "Directory.java")

    def test_rejects_non_java_file(self):
        text_file = self.workspace / "notes.txt"
        text_file.write_text("not Java", encoding="utf-8")

        with self.assertRaisesRegex(FileParseError, "not a .java file"):
            read_file(self.workspace, "notes.txt")

    def test_rejects_invalid_utf8(self):
        java_file = self.workspace / "Invalid.java"
        java_file.write_bytes(b"\xff\xfe")

        with self.assertRaisesRegex(FileParseError, "not valid UTF-8"):
            read_file(self.workspace, "Invalid.java")

    def test_truncates_content_above_limit(self):
        java_file = self.workspace / "Large.java"
        java_file.write_text("abcdef", encoding="utf-8")

        result = read_file(self.workspace, "Large.java", max_char=5)

        self.assertEqual("abcde", result["content"])
        self.assertTrue(result["truncated"])

    def test_does_not_truncate_content_at_limit(self):
        java_file = self.workspace / "Exact.java"
        java_file.write_text("abcde", encoding="utf-8")

        result = read_file(self.workspace, "Exact.java", max_char=5)

        self.assertEqual("abcde", result["content"])
        self.assertFalse(result["truncated"])


if __name__ == "__main__":
    unittest.main()
