from logging import Logger

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models._models import Connection
from azure.identity import DefaultAzureCredential
from azure.identity._credentials.chained import ChainedTokenCredential
from azure.ai.evaluation import AzureOpenAIModelConfiguration, GroundednessEvaluator, ContentSafetyEvaluator, QAEvaluator
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer

from ai_evaluator.configuration.config import Config
from ai_evaluator.configuration.logs import LoggingConfig
from ai_evaluator.configuration.os_environ.azure_ai_project import AzureAIProjectSettings
from ai_evaluator.configuration.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.configuration.os_environ.settings import Settings
from ai_evaluator.configuration.os_environ.utils import load_dotenv_files


async def get_connection_async(container: ReadableContainer) -> Connection:
    client: AIProjectClient = container[AIProjectClient]
    return await client.connections.get_default(connection_type="AzureOpenAI")

container = Container()

load_dotenv_files()  # FIXME? move to main.py?

container[Config] = Singleton(Config())
container[LoggingConfig] = lambda c: c[Config].logging
container[Logger] = lambda c: c[LoggingConfig].logger

container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai
container[AzureAIProjectSettings] = lambda c: c[Settings].azure_ai_project

container[AIProjectClient] = lambda c: AIProjectClient(
    credential=c[ChainedTokenCredential],  # pyright: ignore[reportArgumentType]
    endpoint=c[AzureAIProjectSettings].endpoint,
    subscription_id=c[AzureAIProjectSettings].subscription_id,
    resource_group_name=c[AzureAIProjectSettings].resource_group_name,
    project_name=c[AzureAIProjectSettings].project_name,
)

# TODO use Connection settings. # NOTE: Connection is async tho
# fmt: off
container[AzureOpenAIModelConfiguration] = lambda c: AzureOpenAIModelConfiguration(
    azure_endpoint=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,  # FIXME use Connection instead
    azure_deployment=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version)
# fmt: on

container[ChainedTokenCredential] = DefaultAzureCredential


container[GroundednessEvaluator] = lambda c: GroundednessEvaluator(model_config=c[AzureOpenAIModelConfiguration])

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#composite-evaluators
# NOTE: Includes
# - CoherenceEvaluator
# - FluencyEvaluator
# - F1ScoreEvaluator
# - GroundednessEvaluator
# - RelevanceEvaluator
# - SimilarityEvaluator
container[QAEvaluator] = lambda c: QAEvaluator(model_config=c[AzureOpenAIModelConfiguration])

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#composite-evaluators
# NOTE: Includes
# - HateUnfairnessEvaluator
# - SelfHarmEvaluator
# - SexualEvaluator
# - ViolenceEvaluator
container[ContentSafetyEvaluator] = lambda c: ContentSafetyEvaluator(
    azure_ai_project=c[AIProjectClient],
    credential=c[ChainedTokenCredential],
    model_config=c[AzureOpenAIModelConfiguration]
)

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#evaluator-parameter-format
container[dict[str, EvaluatorBase[str | float]]] = lambda c: {
    "qa": c[QAEvaluator],
    # "content_safety": c[ContentSafetyEvaluator],
}

container[dict[str, EvaluatorConfig]] = lambda c: {
    "groundedness": {  # EvaluatorConfig(  # TODO TypedDict
        "query": "${data.queries}",
        "context": "${data.context}",
        "response": "${data.response}",
    }
}
