from logging import Logger

from azure.ai.evaluation import AzureOpenAIModelConfiguration, GroundednessEvaluator
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from lagom import Container, Singleton

from ai_evaluator.configuration.config import Config
from ai_evaluator.configuration.logs import LoggingConfig
from ai_evaluator.configuration.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.configuration.os_environ.settings import Settings
from ai_evaluator.configuration.os_environ.utils import load_dotenv_files

container = Container()

load_dotenv_files()  # FIXME? move to main.py?

container[Config] = Singleton(Config())
container[LoggingConfig] = lambda c: c[Config].logging
container[Logger] = lambda c: c[LoggingConfig].logger

container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai


# fmt: off
container[AzureOpenAIModelConfiguration] = lambda c: AzureOpenAIModelConfiguration(
    azure_endpoint=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,
    azure_deployment=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version)
# fmt: on

container[GroundednessEvaluator] = lambda c: GroundednessEvaluator(model_config=c[AzureOpenAIModelConfiguration])

container[list[EvaluatorBase[str | float]]] = lambda c: [c[GroundednessEvaluator]]
