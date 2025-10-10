from logging import Logger

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.tasks.task_store import TaskStore
from agent_framework import ChatClientProtocol, ConcurrentBuilder, Workflow
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from lagom import Container, Singleton
from starlette.applications import Starlette

from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.protocol import ChatAgentRunnerProtocol
from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.agent_framework.builtin.workflow.runner.protocol import WorkflowRunnerProtocol
from agent_framework_sampler.agent_framework.builtin.workflow.runner.runner import WorkflowRunner
from agent_framework_sampler.ai.a2a.agent_framework.chat_agent.executor import ChatA2AgentFrameworkRunnerExecutor
from agent_framework_sampler.ai.a2a.agent_framework.workflow.executor import WorkflowA2AgentFrameworkRunnerExecutor
from agent_framework_sampler.ai.modules.chemistry_expert.agent_framework.agent.v1 import ChemistryExpertChatAgent
from agent_framework_sampler.ai.modules.experts_panel.a2a.cards import ExpertsPanelA2AgentCards
from agent_framework_sampler.ai.modules.physics_expert.agent_framework.agent.v1 import PhysicsExpertChatAgent
from agent_framework_sampler.ai.modules.weather.a2a.cards import WeatherA2AgentCards
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

### Chat Agents ###

container[WeatherChatAgent] = lambda c: WeatherChatAgent(
    chat_client=c[ChatClientProtocol],
)

container[PhysicsExpertChatAgent] = lambda c: PhysicsExpertChatAgent(
    chat_client=c[ChatClientProtocol],
)

container[ChemistryExpertChatAgent] = lambda c: ChemistryExpertChatAgent(
    chat_client=c[ChatClientProtocol],
)

### Agent Runner(s) ###

container[ThreadedChatAgentRunner] = lambda c: ThreadedChatAgentRunner(
    chat_agent=c[WeatherChatAgent],
)

container[ChatAgentRunnerProtocol] = lambda c: c[ThreadedChatAgentRunner]


### Orchestration ###

container[ConcurrentBuilder] = ConcurrentBuilder

ExpertsPanelWorkflow = Workflow

# fmt: off
container[ExpertsPanelWorkflow] = lambda c: c[ConcurrentBuilder] \
    .participants(
        [
            c[PhysicsExpertChatAgent],
            c[ChemistryExpertChatAgent],
        ]
    ) \
    .build()
# fmt: on

container[WorkflowRunner] = lambda c: WorkflowRunner(
    workflow=c[ExpertsPanelWorkflow],
)

container[WorkflowRunnerProtocol] = lambda c: c[WorkflowRunner]

### A2A Server ###

container[WeatherA2AgentCards] = lambda c: WeatherA2AgentCards(configuration=c[Configuration])
container[ExpertsPanelA2AgentCards] = lambda c: ExpertsPanelA2AgentCards(configuration=c[Configuration])

container[ChatA2AgentFrameworkRunnerExecutor] = lambda c: ChatA2AgentFrameworkRunnerExecutor(agent=c[ChatAgentRunnerProtocol])
container[WorkflowA2AgentFrameworkRunnerExecutor] = lambda c: WorkflowA2AgentFrameworkRunnerExecutor(workflow=c[WorkflowRunnerProtocol])

# Choose either or
# container[AgentExecutor] = lambda c: container[ChatA2AgentFrameworkRunnerExecutor]
container[AgentExecutor] = lambda c: container[WorkflowA2AgentFrameworkRunnerExecutor]

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
    agent_card=c[ExpertsPanelA2AgentCards].agent_card,
    extended_agent_card=c[ExpertsPanelA2AgentCards].extended_agent_card)
# fmt: on


container[Starlette] = lambda c: c[A2AStarletteApplication].build()  # type: ignore  # FIXME
