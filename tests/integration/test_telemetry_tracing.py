from unittest.mock import MagicMock, patch

from flow_portal.config import AgentFramework, TracingConfig
from flow_portal.tracing import RichConsoleSpanExporter


def test_rich_console_span_exporter_default(llm_span):  # type: ignore[no-untyped-def]
    console_mock = MagicMock()
    with patch("flow_portal.tracing.Console", console_mock):
        exporter = RichConsoleSpanExporter(AgentFramework.LANGCHAIN, TracingConfig())
        exporter.export([llm_span])
        console_mock.return_value.rule.assert_called()


def test_rich_console_span_exporter_disable(llm_span):  # type: ignore[no-untyped-def]
    console_mock = MagicMock()
    with patch("flow_portal.tracing.Console", console_mock):
        exporter = RichConsoleSpanExporter(
            AgentFramework.LANGCHAIN,
            TracingConfig(llm=None),
        )
        exporter.export([llm_span])
        console_mock.return_value.rule.assert_not_called()
