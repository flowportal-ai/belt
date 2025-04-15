import pathlib
import pytest
from unittest.mock import MagicMock, patch
from mktestdocs import check_md_file


# Note the use of `str`, makes for pretty output
@pytest.mark.parametrize("fpath", pathlib.Path("docs").glob("**/*.md"), ids=str)
def test_files_all(fpath):
    # Create a mock for evaluate_telemetry
    mock_evaluate = MagicMock()
    mock_agent = MagicMock()
    mock_create = MagicMock(return_value=mock_agent)
    # Patch the evaluate_telemetry function.
    # Eventually we may want to better validate that the docs use evaluate_telemetry correctly
    with patch(
        "flow_portal.evaluation.evaluate.evaluate_telemetry", mock_evaluate
    ), patch("flow_portal.AnyAgent.create", mock_create):
        check_md_file(fpath=fpath, memory=True)
