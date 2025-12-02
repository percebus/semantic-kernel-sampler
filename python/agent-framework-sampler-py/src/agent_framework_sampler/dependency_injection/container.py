from logging import Logger

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.tasks.task_store import TaskStore
from agent_framework import ChatClientProtocol, ConcurrentBuilder, Workflow
from agent_framework.azure import AzureOpenAIChatClient, AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from lagom import Container, Singleton
from starlette.applications import Starlette

from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.protocol import ChatAgentRunnerProtocol
from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.agent_framework.builtin.workflow.runner.protocol import WorkflowRunnerProtocol
from agent_framework_sampler.agent_framework.builtin.workflow.runner.simple import SimpleWorkflowRunner
from agent_framework_sampler.ai.a2a.executors.agent_framework.chat_agent.runner import ChatAgentRunnerA2AgentFrameworkExecutor
from agent_framework_sampler.ai.a2a.executors.agent_framework.workflow.runner import WorkflowRunnerA2AgentFrameworkExecutor
from agent_framework_sampler.ai.a2a.executors.agent_framework.workflow.simple import SimpleWorkflowA2AgentFrameworkExecutor
from agent_framework_sampler.ai.a2a.executors.agent_framework.workflow.streaming import StreamingWorkflowA2AgentFrameworkExecutor
from agent_framework_sampler.ai.modules.chemistry_expert.agent_framework.agent.v1 import ChemistryExpertChatAgent
from agent_framework_sampler.ai.modules.experts_panel.a2a.cards import ExpertsPanelA2AgentCards
from agent_framework_sampler.ai.modules.ms_learn.agent_framework.agent.v1 import MSLearnChatAgent
from agent_framework_sampler.ai.modules.ms_learn.agent_framework.tools.ms_learn import MSLearnMCPStreamableHttpTool
from agent_framework_sampler.ai.modules.physics_expert.agent_framework.agent.v1 import PhysicsExpertChatAgent
from agent_framework_sampler.ai.modules.weather.a2a.cards import WeatherA2AgentCards
from agent_framework_sampler.ai.modules.weather.agent_framework.agent.v2 import WeatherChatAgent_V2
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


# OpenAI new Response API = Chat Completions API + Assistant API
container[AzureOpenAIResponsesClient] = lambda c: AzureOpenAIResponsesClient(
    base_url=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,
    deployment_name=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
    credential=c[AzureCliCredential],
)


# Choose either or
container[ChatClientProtocol] = lambda c: c[AzureOpenAIChatClient]
# container[ChatClientProtocol] = lambda c: c[AzureOpenAIResponsesClient]

container[MSLearnMCPStreamableHttpTool] = lambda c: MSLearnMCPStreamableHttpTool(configuration=c[Configuration])

### Chat Agents ###########################################################

container[WeatherChatAgent_V2] = lambda c: WeatherChatAgent_V2(
    chat_client=c[ChatClientProtocol],
)

container[PhysicsExpertChatAgent] = lambda c: PhysicsExpertChatAgent(
    chat_client=c[ChatClientProtocol],
)

container[ChemistryExpertChatAgent] = lambda c: ChemistryExpertChatAgent(
    chat_client=c[ChatClientProtocol],
)

container[MSLearnChatAgent] = lambda c: MSLearnChatAgent(
    chat_client=c[ChatClientProtocol],
    ms_learn_tool=c[MSLearnMCPStreamableHttpTool],
)

### Agent Runner(s) ###########################################################

container[ThreadedChatAgentRunner] = lambda c: ThreadedChatAgentRunner(
    chat_agent=c[WeatherChatAgent_V2],
)

container[ChatAgentRunnerProtocol] = lambda c: c[ThreadedChatAgentRunner]


### Orchestration ###########################################################

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

container[SimpleWorkflowRunner] = lambda c: SimpleWorkflowRunner(
    workflow=c[ExpertsPanelWorkflow],
)

container[WorkflowRunnerProtocol] = lambda c: c[SimpleWorkflowRunner]

### A2A Server ###########################################################

container[WeatherA2AgentCards] = lambda c: WeatherA2AgentCards(configuration=c[Configuration])
container[ExpertsPanelA2AgentCards] = lambda c: ExpertsPanelA2AgentCards(configuration=c[Configuration])

container[ChatAgentRunnerA2AgentFrameworkExecutor] = lambda c: ChatAgentRunnerA2AgentFrameworkExecutor(runner=c[ChatAgentRunnerProtocol])

container[StreamingWorkflowA2AgentFrameworkExecutor] = lambda c: StreamingWorkflowA2AgentFrameworkExecutor(
    configuration=c[Configuration],
    workflow=c[ExpertsPanelWorkflow],
)

container[SimpleWorkflowA2AgentFrameworkExecutor] = lambda c: SimpleWorkflowA2AgentFrameworkExecutor(
    configuration=c[Configuration],
    workflow=c[ExpertsPanelWorkflow],
)

container[WorkflowRunnerA2AgentFrameworkExecutor] = lambda c: WorkflowRunnerA2AgentFrameworkExecutor(
    configuration=c[Configuration],
    runner=c[WorkflowRunnerProtocol],
)


# Choose either or
# container[AgentExecutor] = lambda c: container[ChatA2AgentFrameworkRunnerExecutor]
# container[AgentExecutor] = lambda c: container[WorkflowRunnerA2AgentFrameworkExecutor]
# container[AgentExecutor] = lambda c: container[SimpleWorkflowA2AgentFrameworkExecutor]
container[AgentExecutor] = lambda c: container[StreamingWorkflowA2AgentFrameworkExecutor]

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
