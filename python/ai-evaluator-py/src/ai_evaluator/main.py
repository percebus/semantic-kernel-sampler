from typing import TYPE_CHECKING

from azure.ai.evaluation import GroundednessEvaluator, evaluate  # pyright: ignore[reportUnknownVariableType]
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from lagom import Container

from ai_evaluator.dependency_injection.container import container
from utils.lodash import noop

if TYPE_CHECKING:
    from azure.ai.evaluation._evaluate._evaluate import EvaluationResult  # pyright: ignore[reportPrivateImportUsage]


def run(ctr: Container) -> None:
    evaluators: dict[str, EvaluatorBase[str | float]] = {}
    for oEvaluator in ctr[list[EvaluatorBase[str | float]]]:
        evaluators[oEvaluator.__class__.__name__] = oEvaluator

    evaluator_configurations = {}
    evaluator_configurations[GroundednessEvaluator.__name__] = {
        "query": "${data.queries}",
        "context": "${data.context}",
        "response": "${data.response}",
    }

    dataset_path: str = "./assets/examples/01_turn_on_the_light/03_experiments/01/01_responses/turns.jsonl"
    # dataset_path: str = "./assets/examples/01_turn_on_the_light/03_experiments/01/03_dataset/conversations.jsonl"
    oEvaluationResult: EvaluationResult = evaluate(
        data=dataset_path,
        evaluators=evaluators,  #  # pyright: ignore[reportArgumentType]
        evaluator_config=evaluator_configurations,  # pyright: ignore[reportUnknownArgumentType]
        output_path="data/output/evaluation_results.jsonl",
        # azure_ai_project=None  # TODO
    )

    noop(oEvaluationResult)


def main() -> None:
    run(container)


if __name__ == "__main__":
    main()
