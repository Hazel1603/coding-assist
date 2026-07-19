import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from cd_assist.agent import (
    CodingAssistantAgent,
    ModelResponseError,
    generate_response,
)


FIXTURE_WORKSPACE = Path(__file__).parent / "fixtures"


class CodingAssistantAgentTests(unittest.TestCase):
    def test_explain_file_sends_java_file_to_model(self):
        client = object()
        model_callback = Mock(return_value="ExampleService is an empty class.")
        agent = CodingAssistantAgent(client, FIXTURE_WORKSPACE, model_callback)

        result = agent.explain_file("ExampleService.java")

        self.assertEqual("ExampleService is an empty class.", result)
        callback_client, prompt = model_callback.call_args.args
        self.assertIs(client, callback_client)
        self.assertIn("File: ExampleService.java", prompt)
        self.assertIn("public class ExampleService", prompt)
        self.assertIn("Purpose", prompt)
        self.assertIn("Evidence", prompt)
        self.assertIn("Inference", prompt)
        self.assertIn("at most 200 words", prompt)


class GenerateResponseTests(unittest.TestCase):
    @patch("cd_assist.agent.client_config.MODEL_NAME", "test-model")
    def test_combines_streamed_text(self):
        events = [
            SimpleNamespace(type="response.output_text.delta", delta="Hello "),
            SimpleNamespace(type="response.output_text.delta", delta="world"),
            SimpleNamespace(type="response.completed"),
        ]
        client = Mock()
        client.responses.create.return_value = events

        result = generate_response(client, "Explain this file")

        self.assertEqual("Hello world", result)
        client.responses.create.assert_called_once_with(
            model="test-model",
            input="Explain this file",
            stream=True,
        )

    def test_raises_when_stream_does_not_complete(self):
        client = Mock()
        client.responses.create.return_value = [
            SimpleNamespace(type="response.failed")
        ]

        with self.assertRaisesRegex(ModelResponseError, "did not complete"):
            generate_response(client, "Explain this file")


if __name__ == "__main__":
    unittest.main()
