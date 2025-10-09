from logging import Logger

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.tasks.task_store import TaskStore
from agent_framework import ChatClientProtocol
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from lagom import Container, Singleton
from starlette.applications import Starlette

from agent_framework_sampler.ai.a2a.agent_framework.agent.executor import A2AgentInvokerExecutor
from agent_framework_sampler.ai.a2a.agent_framework.agent.protocol import A2AgentFrameworkRunnerProtocol
from agent_framework_sampler.ai.modules.weather.a2agent import WeatherA2AgentRunner
from agent_framework_sampler.ai.modules.weather.agent_framework.agent.v1 import WeatherChatAgent
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


container[WeatherA2AgentRunner] = lambda c: WeatherA2AgentRunner(
    configuration=c[Configuration],
    chat_agent=c[WeatherChatAgent],
)

container[A2AgentFrameworkRunnerProtocol] = lambda c: c[WeatherA2AgentRunner]

container[AgentExecutor] = lambda c: A2AgentInvokerExecutor(agent=c[A2AgentFrameworkRunnerProtocol])

# Where to store Tasks
container[TaskStore] = InMemoryTaskStore

# fmt: off
container[RequestHandler] = lambda c: DefaultRequestHandler(
    task_store=c[TaskStore],
    agent_executor=c[AgentExecutor])
# fmt: on

# fmt: off
container[A2AStarletteApplication] = lambda c: A2AStarletteApplication(
    http_handler=c[RequestHandler],
    agent_card=c[A2AgentFrameworkRunnerProtocol].agent_card,
    extended_agent_card=c[A2AgentFrameworkRunnerProtocol].extended_agent_card)
# fmt: on


container[Starlette] = lambda c: c[A2AStarletteApplication].build()  # type: ignore  # FIXME
