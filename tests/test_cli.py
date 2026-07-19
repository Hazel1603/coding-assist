import unittest
from unittest.mock import Mock, patch

from cd_assist.cli import handle_explain_command
from cd_assist.tools import FileParseError


class HandleExplainCommandTests(unittest.TestCase):
    @patch("cd_assist.cli.print_agent_response")
    @patch("cd_assist.cli.print_exception")
    def test_reports_missing_file(self, print_exception, print_agent_response):
        agent = Mock()
        error = FileParseError("Path provided is not a file")
        agent.explain_file.side_effect = error

        handle_explain_command("explain Missing.java", agent)

        agent.explain_file.assert_called_once_with("Missing.java")
        print_exception.assert_called_once_with(error)
        print_agent_response.assert_not_called()


if __name__ == "__main__":
    unittest.main()
