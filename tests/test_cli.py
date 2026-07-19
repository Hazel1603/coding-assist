import unittest
from unittest.mock import Mock, patch

from cd_assist.agent import ModelResponseError
from cd_assist.cli import handle_ask_command, handle_explain_command, run_app
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


class HandleAskCommandTests(unittest.TestCase):
    @patch("cd_assist.cli.print_agent_response")
    @patch("cd_assist.cli.build_working_context")
    @patch("cd_assist.cli.search_files")
    def test_searches_builds_context_and_asks_agent(
        self,
        search_files,
        build_working_context,
        print_agent_response,
    ):
        agent = Mock()
        search_results = [object()]
        search_files.return_value = search_results
        build_working_context.return_value = "working context"
        agent.ask_question.return_value = "agent answer"

        handle_ask_command("ask validation", agent, "workspace")

        search_files.assert_called_once_with("workspace", "validation")
        build_working_context.assert_called_once_with(search_results)
        agent.ask_question.assert_called_once_with("validation", "working context")
        print_agent_response.assert_called_once_with("agent answer")

    @patch("cd_assist.cli.print_agent_response")
    @patch("cd_assist.cli.print_exception")
    @patch("cd_assist.cli.build_working_context", return_value="working context")
    @patch("cd_assist.cli.search_files", return_value=[])
    def test_reports_model_error(
        self,
        search_files,
        build_working_context,
        print_exception,
        print_agent_response,
    ):
        agent = Mock()
        error = ModelResponseError("Could not generate a model response")
        agent.ask_question.side_effect = error

        handle_ask_command("ask validation", agent, "workspace")

        print_exception.assert_called_once_with(error)
        print_agent_response.assert_not_called()

    @patch("cd_assist.cli.print_no_query")
    def test_reports_missing_query(self, print_no_query):
        agent = Mock()

        handle_ask_command("ask", agent, "workspace")

        print_no_query.assert_called_once_with()
        agent.ask_question.assert_not_called()

    @patch("cd_assist.cli.print_agent_response")
    @patch("cd_assist.cli.print_exception")
    @patch("cd_assist.cli.search_files")
    def test_reports_search_error(
        self,
        search_files,
        print_exception,
        print_agent_response,
    ):
        agent = Mock()
        error = FileParseError("Workspace is not a directory")
        search_files.side_effect = error

        handle_ask_command("ask validation", agent, "workspace")

        print_exception.assert_called_once_with(error)
        agent.ask_question.assert_not_called()
        print_agent_response.assert_not_called()


class RunAppTests(unittest.TestCase):
    @patch("cd_assist.cli.print_goodbye")
    @patch("cd_assist.cli.print_intro")
    @patch("cd_assist.cli.handle_explain_command")
    @patch("cd_assist.cli.handle_ask_command")
    @patch("builtins.input", side_effect=["ask validation", "explain Example.java", "exit"])
    def test_routes_ask_and_explain_commands(
        self,
        input_mock,
        handle_ask_command,
        handle_explain_command,
        print_intro,
        print_goodbye,
    ):
        agent = Mock()

        run_app(object(), "workspace", agent)

        handle_ask_command.assert_called_once_with("ask validation", agent, "workspace")
        handle_explain_command.assert_called_once_with("explain Example.java", agent)
        print_goodbye.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
