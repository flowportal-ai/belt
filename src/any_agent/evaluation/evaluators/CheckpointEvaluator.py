from collections.abc import Sequence
from typing import TYPE_CHECKING

from flow_portal.evaluation.evaluators.LLMEvaluator import LLMEvaluator
from flow_portal.evaluation.evaluators.schemas import EvaluationResult
from flow_portal.evaluation.test_case import CheckpointCriteria
from flow_portal.logging import logger
from flow_portal.tracing.processors.base import TracingProcessor

if TYPE_CHECKING:
    from flow_portal.tracing.trace import AgentTrace


class CheckpointEvaluator(LLMEvaluator):
    """Evaluates checkpoints against trace."""

    def evaluate(
        self,
        trace: "AgentTrace",
        checkpoints: Sequence[CheckpointCriteria],
        processor: TracingProcessor,
    ) -> list[EvaluationResult]:
        """Verify each checkpoint against the trace data using LLM.

        Args:
            trace: The trace data to evaluate
            checkpoints: List of checkpoint criteria to verify
            processor: Trace processor to extract evidence

        Returns:
            List of evaluation results

        """
        evidence = processor.extract_evidence(trace)
        evidence = evidence.replace("<", "\\<").replace(">", "\\>")
        logger.info(f"""<yellow>Evidence\n{evidence}</yellow>\n""")
        results = []

        for checkpoint in checkpoints:
            evaluation = self.llm_evaluate_with_criterion(
                criteria=checkpoint.criteria,
                points=checkpoint.points,
                evidence=evidence,
            )
            results.append(evaluation)

        return results
