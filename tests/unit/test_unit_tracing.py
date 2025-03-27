from unittest.mock import patch, MagicMock

import pytest

from flow_portal.tracing import get_tracer_provider, setup_tracing
from flow_portal.schema import AgentFramework


def test_get_tracer_provider(tmp_path):
    mock_trace = MagicMock()
    mock_tracer_provider = MagicMock()

    with (
        patch("flow_portal.tracing.trace", mock_trace),
        patch("flow_portal.tracing.TracerProvider", mock_tracer_provider),
    ):
        get_tracer_provider(
            project_name="test_project",
            output_dir=tmp_path / "telemetry",
            agent_framework=AgentFramework.OPENAI,
        )
        assert (tmp_path / "telemetry").exists()
        mock_trace.set_tracer_provider.assert_called_once_with(
            mock_tracer_provider.return_value
        )


def test_invalid_agent_framework():
    with pytest.raises(NotImplementedError, match="tracing is not supported"):
        setup_tracing(MagicMock(), "invalid_agent_framework")
