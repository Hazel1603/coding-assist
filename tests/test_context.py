import unittest

from cd_assist.context import FileContext, build_working_context
from cd_assist.tools import LineSnippet, MatchType, SearchResult


class FileContextTests(unittest.TestCase):
    def test_generates_file_heading_and_line_snippets(self):
        context = FileContext(
            file_name="service/UserService.java",
            snippets=[
                LineSnippet(line=12, snippet="User findUser(String id)\n"),
                LineSnippet(line=30, snippet="validateUser(user)\n"),
            ],
        )

        result = context.generate_context()

        self.assertEqual(
            "File: service/UserService.java\n\n"
            "Line 12:\nUser findUser(String id)\n\n"
            "Line 30:\nvalidateUser(user)",
            result,
        )

    def test_uses_a_separate_default_snippet_list_per_file(self):
        first = FileContext("First.java")
        second = FileContext("Second.java")

        first.snippets.append(LineSnippet(line=1, snippet="first"))

        self.assertEqual([], second.snippets)


class BuildWorkingContextTests(unittest.TestCase):
    def test_groups_matches_by_file_and_sorts_files_and_lines(self):
        search_results = [
            SearchResult(
                path="Zebra.java",
                match_type=MatchType.CONTENT,
                line_snippet=LineSnippet(line=9, snippet="zebra"),
            ),
            SearchResult(
                path="Alpha.java",
                match_type=MatchType.CONTENT,
                line_snippet=LineSnippet(line=8, snippet="later"),
            ),
            SearchResult(
                path="Alpha.java",
                match_type=MatchType.CONTENT,
                line_snippet=LineSnippet(line=2, snippet="earlier"),
            ),
        ]

        result = build_working_context(search_results)

        self.assertLess(result.index("File: Alpha.java"), result.index("File: Zebra.java"))
        self.assertLess(result.index("Line 2:"), result.index("Line 8:"))
        self.assertEqual(1, result.count("File: Alpha.java"))
        self.assertIn("Context truncated: False", result)

    def test_includes_a_file_that_only_has_a_path_match(self):
        search_results = [
            SearchResult(path="UserService.java", match_type=MatchType.PATH)
        ]

        result = build_working_context(search_results)

        self.assertIn("File: UserService.java", result)
        self.assertIn("Context truncated: False", result)

    def test_returns_a_non_truncated_empty_context(self):
        result = build_working_context([])

        self.assertEqual("Context truncated: False", result)

    def test_marks_context_as_truncated_when_content_exceeds_budget(self):
        search_results = [
            SearchResult(
                path="Example.java",
                match_type=MatchType.CONTENT,
                line_snippet=LineSnippet(line=1, snippet="x" * 100),
            )
        ]

        result = build_working_context(search_results, max_chars=30)

        self.assertLessEqual(len(result), 30)
        self.assertTrue(result.endswith("Context truncated: True"))

    def test_rejects_content_match_without_line_snippet(self):
        search_results = [
            SearchResult(path="Example.java", match_type=MatchType.CONTENT)
        ]

        with self.assertRaisesRegex(ValueError, "requires a line snippet"):
            build_working_context(search_results)

    def test_rejects_content_match_without_line_number(self):
        search_results = [
            SearchResult(
                path="Example.java",
                match_type=MatchType.CONTENT,
                line_snippet=LineSnippet(snippet="example"),
            )
        ]

        with self.assertRaisesRegex(ValueError, "requires a line snippet"):
            build_working_context(search_results)


if __name__ == "__main__":
    unittest.main()
