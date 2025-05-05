import pathlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mktestdocs import check_md_file


# Note the use of `str`, makes for pretty output
@pytest.mark.parametrize("fpath", pathlib.Path("docs").glob("**/*.md"), ids=str)
def test_files_all(fpath: pathlib.Path) -> None:
    mock_agent = MagicMock()
    mock_create = MagicMock(return_value=mock_agent)

    mock_create_async = AsyncMock()
    # Mocking the sav_eval results function so that no actual file is created from running the code in evaluation.md
    with (
        patch(
            "flow_portal.evaluation.evaluation_runner.save_evaluation_results",
            return_value=None,
        ),
        patch("flow_portal.evaluation.evaluation_runner.EvaluationRunner.run"),
        patch("flow_portal.AnyAgent.create", mock_create),
        patch("flow_portal.AnyAgent.create_async", mock_create_async),
    ):
        check_md_file(fpath=fpath, memory=True)  # type: ignore[no-untyped-call]
