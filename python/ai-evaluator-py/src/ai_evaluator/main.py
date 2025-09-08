from typing import TYPE_CHECKING

from azure.ai.evaluation import evaluate  # pyright: ignore[reportUnknownVariableType]
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from lagom import Container

from ai_evaluator.dependency_injection.container import container
from ai_evaluator.utils.lodash import noop

if TYPE_CHECKING:
    from azure.ai.evaluation._evaluate._evaluate import EvaluationResult  # pyright: ignore[reportPrivateImportUsage]


def run(ctr: Container) -> None:

    dataset_path: str = "./assets/examples/01_turn_on_the_light/03_experiments/01/01_responses/turns.jsonl"
    # dataset_path: str = "./assets/examples/01_turn_on_the_light/03_experiments/01/03_dataset/conversations.jsonl"

    evaluators: dict[str, EvaluatorBase[str | float]] = ctr[dict[str, EvaluatorBase[str | float]]]
    evaluator_configurations: dict[str, EvaluatorConfig] = ctr[dict[str, EvaluatorConfig]]
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
