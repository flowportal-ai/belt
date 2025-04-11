from typing import Dict, List, Any

from flow_portal.evaluation.evaluators.LLMEvaluator import LLMEvaluator
from flow_portal.evaluation.evaluators.schemas import EvaluationResult
from flow_portal.telemetry import TelemetryProcessor
from flow_portal.evaluation.test_case import CheckpointCriteria
from flow_portal.logging import logger


class CheckpointEvaluator(LLMEvaluator):
    """Evaluates checkpoints against telemetry"""

    def evaluate(
        self,
        telemetry: List[Dict[str, Any]],
        checkpoints: List[CheckpointCriteria],
        processor: TelemetryProcessor,
    ) -> List[EvaluationResult]:
        """
        Verify each checkpoint against the telemetry data using LLM

        Args:
            telemetry: The telemetry data to evaluate
            checkpoints: List of checkpoint criteria to verify
            processor: Telemetry processor to extract evidence

        Returns:
            List of evaluation results
        """
        evidence = processor.extract_evidence(telemetry)
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
