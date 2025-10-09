from logging import Logger

from agent_framework import ChatClientProtocol
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from lagom import Container, Singleton

from agent_framework_sampler.ai.modules.weather.ms.agent.v1 import WeatherChatAgent
from agent_framework_sampler.config.configuration import Configuration
from agent_framework_sampler.config.logs import LoggingConfig
from agent_framework_sampler.config.os_environ.settings import A2ASettings, AzureOpenAISettings, Settings
from agent_framework_sampler.config.os_environ.utils import load_dotenv_files

container = Container()

load_dotenv_files()  # TODO move to a __main__.py?
# TODO? Remove all default_factory and initialize here?
container[Configuration] = Singleton(Configuration())
container[LoggingConfig] = lambda c: c[Configuration].logging
container[Logger] = lambda c: c[LoggingConfig].logger

container[Settings] = lambda c: c[Configuration].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai
container[A2ASettings] = lambda c: c[Settings].a2a


container[AzureCliCredential] = AzureCliCredential
container[AzureOpenAIChatClient] = lambda c: AzureOpenAIChatClient(
    base_url=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,
    deployment_name=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
    credential=c[AzureCliCredential],
)

container[ChatClientProtocol] = lambda c: c[AzureOpenAIChatClient]

container[WeatherChatAgent] = lambda c: WeatherChatAgent(
    chat_client=c[ChatClientProtocol],
)
