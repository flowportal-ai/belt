from unittest.mock import patch, MagicMock

import pytest

from flow_portal.tracing import _get_tracer_provider, setup_tracing
from flow_portal.config import AgentFramework, TracingConfig


def test_get_tracer_provider(tmp_path):
    mock_trace = MagicMock()
    mock_tracer_provider = MagicMock()

    with (
        patch("flow_portal.tracing.trace", mock_trace),
        patch("flow_portal.tracing.TracerProvider", mock_tracer_provider),
    ):
        _get_tracer_provider(
            output_dir=tmp_path / "traces",
            agent_framework=AgentFramework.OPENAI,
            tracing_config=TracingConfig(),
        )
        assert (tmp_path / "traces").exists()
        mock_trace.set_tracer_provider.assert_called_once_with(
            mock_tracer_provider.return_value
        )


def test_invalid_agent_framework(tmp_path):
    with pytest.raises(ValueError, match="Unsupported agent type"):
        setup_tracing(MagicMock(), tmp_path / "traces")
