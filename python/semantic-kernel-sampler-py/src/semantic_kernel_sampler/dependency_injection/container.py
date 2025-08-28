from logging import Logger
from typing import Optional
from venv import create

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.tasks.task_store import TaskStore
from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel import Kernel
from semantic_kernel.agents import (  # pylint: disable=no-name-in-module
    GroupChatManager,
    GroupChatOrchestration,
    HandoffOrchestration,
    OrchestrationHandoffs,
    RoundRobinGroupChatManager,
)
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from starlette.applications import Starlette

from semantic_kernel_sampler.ai.a2a.sk.invokers.single.executor import A2AgentInvokerExecutor
from semantic_kernel_sampler.ai.a2a.sk.invokers.single.protocol import SemanticA2AInvokerProtocol
from semantic_kernel_sampler.ai.modules.basic.sk.agent.v2 import BasicChatCompletionAgent
from semantic_kernel_sampler.ai.modules.content_reviewer.sk.agent.v2 import ContentReviewerChatCompletionAgent
from semantic_kernel_sampler.ai.modules.content_writer.sk.agent.v2 import ContentWriterChatCompletionAgent
from semantic_kernel_sampler.ai.modules.light.a2agent import LightCustomSemanticA2AgentInvoker
from semantic_kernel_sampler.ai.modules.light.sk.agent.v3 import LightChatCompletionAgent
from semantic_kernel_sampler.ai.modules.light.sk.plugin.v1 import LightPlugin
from semantic_kernel_sampler.ai.modules.math.sk.agent.v3 import MathChatCompletionAgent
from semantic_kernel_sampler.ai.modules.math.sk.plugin.v1 import MathPlugin
from semantic_kernel_sampler.ai.modules.mcp.demo.a2agent import DemoStdioMCPCustomSemanticA2Agent
from semantic_kernel_sampler.ai.modules.mcp.demo.sk.agent.v3 import DemoMCPChatCompletionAgent
from semantic_kernel_sampler.ai.modules.mcp.demo.sk.plugin.stdio import DemoStdioMCPPlugin
from semantic_kernel_sampler.ai.modules.mcp.mslearn.sk.agent.v1 import MsLearnMCPChatCompletionAgent
from semantic_kernel_sampler.ai.modules.mcp.rest_app.posts.sk.agent.v3 import BlogPostsMCPChatCompletionAgent
from semantic_kernel_sampler.ai.modules.mcp.rest_app.posts.sk.plugin.http import BlogPostsStreamableHttpMCPPlugin
from semantic_kernel_sampler.ai.modules.mcp.rest_app.posts.sk.plugin.stdio import BlogPostsStdioMCPPlugin
from semantic_kernel_sampler.ai.modules.triage.sk.agent.v1 import TriageChatCompletionAgent
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.logs import LoggingConfig
from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.sk.agents.builtin.contents.agent.function import FunctionObservabilityTracker
from semantic_kernel_sampler.sk.agents.builtin.contents.agent.protocol import AgentResponseProtocol
from semantic_kernel_sampler.sk.agents.builtin.contents.agent.simple import SimpleObservabilityTracker
from semantic_kernel_sampler.sk.agents.builtin.contents.human.cli import InputHumanResponse
from semantic_kernel_sampler.sk.agents.builtin.contents.human.protocol import HumanResponseProtocol
from semantic_kernel_sampler.sk.agents.builtin.orchestration.group import GroupChatBuiltinOrchestrationInvoker
from semantic_kernel_sampler.sk.agents.builtin.orchestration.handoff import HandoffBuiltinOrchestrationInvoker
from semantic_kernel_sampler.sk.agents.custom.chat.invoker import CustomSemanticChatInvoker
from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol
from semantic_kernel_sampler.third_party.microsoft.learn.api.mcp import LearnSiteMCPStreamableHttpPlugin, createMCPStreamableHttpPlugin


def createKernel(c: ReadableContainer, plugins: Optional[list[PluginProtocol]] = None) -> Kernel:
    oKernel = Kernel()

    oChatCompletion = c[ChatCompletionClientBase]
    oKernel.add_service(oChatCompletion)

    for plugin in plugins or []:
        oKernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    return oKernel


def createChatHistory(c: ReadableContainer, system_message: Optional[str] = None) -> ChatHistory:
    oChatHistory = ChatHistory()

    if system_message:
        oChatHistory.add_system_message(system_message)

    return oChatHistory


def createOrchestrationHandoffs(c: ReadableContainer) -> OrchestrationHandoffs:
    triageAgent = c[TriageChatCompletionAgent]

    mathAgent = c[MathChatCompletionAgent]
    basicAgent = c[BasicChatCompletionAgent]
    lightAgent = c[LightChatCompletionAgent]

    # fmt: off
    return OrchestrationHandoffs() \
        .add_many(
            source_agent=triageAgent.name,
            target_agents={
                mathAgent.name:
                    "Transfer to this agent when the request is related to basic mathematical calculations (add, substract, multiply, divide)",
                lightAgent.name: "Transfer to this agent when the request is related to a light switch and or light bulb (turn on/off the light)",
                basicAgent.name: "Transfer to this agent when the request is a general culture and/or trivia question"
        }) \
        .add(
            source_agent=mathAgent.name,
            target_agent=triageAgent.name,
            description=
                "Transfer back to this agent when the request is NOT related to basic mathematical calculations (add, substract, multiply, divide)") \
        .add(
            source_agent=lightAgent.name,
            target_agent=triageAgent.name,
            description="Transfer to this agent when the request is NOT related to a light switch and or light bulb")  \
        .add(
            source_agent=basicAgent.name,
            target_agent=triageAgent.name,
            description="Transfer to this agent when the request is NOT a general culture")
    # fmt: on


container = Container()

load_dotenv_files()  # TODO move to a __main__.py?
# TODO? Remove all default_factory and initialize here?
container[Config] = Singleton(Config())
container[LoggingConfig] = lambda c: c[Config].logging
container[Logger] = lambda c: c[LoggingConfig].logger

container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai
container[A2ASettings] = lambda c: c[Settings].a2a

container[MathPlugin] = MathPlugin
container[LightPlugin] = LightPlugin
container[DemoStdioMCPPlugin] = lambda c: DemoStdioMCPPlugin(logger=c[Logger])
container[BlogPostsStdioMCPPlugin] = lambda c: BlogPostsStdioMCPPlugin(logger=c[Logger])
container[BlogPostsStreamableHttpMCPPlugin] = BlogPostsStreamableHttpMCPPlugin
container[LearnSiteMCPStreamableHttpPlugin] = createMCPStreamableHttpPlugin

# NOTE: If you need all Plugins for w/e reason
# fmt: off
container[list[PluginProtocol]] = lambda c: [
    c[MathPlugin],
    c[LightPlugin],
    c[DemoStdioMCPPlugin],
    c[BlogPostsStreamableHttpMCPPlugin],
    c[LearnSiteMCPStreamableHttpPlugin]
]
# fmt: on

container[ChatHistory] = lambda c: createChatHistory(c)  # pylint: disable=unnecessary-lambda

container[FunctionChoiceBehavior] = FunctionChoiceBehavior.Auto()  # pyright: ignore[reportUnknownMemberType]

container[PromptExecutionSettings] = lambda c: AzureChatPromptExecutionSettings(
    function_choice_behavior=c[FunctionChoiceBehavior]  # pyright: ignore[reportUnknownMemberType]
)

container[AzureChatCompletion] = lambda c: AzureChatCompletion(
    base_url=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,
    deployment_name=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
)

container[ChatCompletionClientBase] = lambda c: c[AzureChatCompletion]

container[Kernel] = lambda c: createKernel(c)  # pylint: disable=unnecessary-lambda


container[BasicChatCompletionAgent] = lambda c: BasicChatCompletionAgent(
    kernel=createKernel(c),
)

container[ContentWriterChatCompletionAgent] = lambda c: ContentWriterChatCompletionAgent(
    kernel=createKernel(c),
)

container[ContentReviewerChatCompletionAgent] = lambda c: ContentReviewerChatCompletionAgent(
    kernel=createKernel(c),
)

container[LightChatCompletionAgent] = lambda c: LightChatCompletionAgent(
    kernel=createKernel(c, [c[LightPlugin]]),
)

container[MathChatCompletionAgent] = lambda c: MathChatCompletionAgent(
    kernel=createKernel(c, [c[MathPlugin]]),
)

container[MsLearnMCPChatCompletionAgent] = lambda c: MsLearnMCPChatCompletionAgent(
    kernel=createKernel(c, [c[LearnSiteMCPStreamableHttpPlugin]]),
)

container[DemoMCPChatCompletionAgent] = lambda c: DemoMCPChatCompletionAgent(
    kernel=createKernel(c, [c[DemoStdioMCPPlugin]]),
)

container[BlogPostsMCPChatCompletionAgent] = lambda c: BlogPostsMCPChatCompletionAgent(
    kernel=createKernel(c, [
        # NOTE: Choose one or the other
        # c[BlogPostsStdioMCPPlugin]
        c[BlogPostsStreamableHttpMCPPlugin]
    ]),
)


container[TriageChatCompletionAgent] = lambda c: TriageChatCompletionAgent(
    kernel=createKernel(c),
)


container[CustomSemanticChatInvoker] = lambda c: CustomSemanticChatInvoker(
    kernel=createKernel(c),  # NOTE: No plugins
    chat_history=createChatHistory(c, system_message=c[LightChatCompletionAgent].instructions),
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
)


container[InProcessRuntime] = InProcessRuntime

container[GroupChatManager] = lambda: RoundRobinGroupChatManager(max_rounds=5)

container[OrchestrationHandoffs] = createOrchestrationHandoffs

container[SimpleObservabilityTracker] = lambda c: SimpleObservabilityTracker(logger=c[Logger])

container[FunctionObservabilityTracker] = lambda c: FunctionObservabilityTracker(logger=c[Logger])

# Default Tracker for Agents
container[AgentResponseProtocol] = lambda c: c[FunctionObservabilityTracker]

container[InputHumanResponse] = lambda c: InputHumanResponse(logger=c[Logger])

# Default Input for Agents
container[HumanResponseProtocol] = lambda c: c[InputHumanResponse]


# NOTE: Agents don't have plugins, so we use the lightweight kernel SimpleObservabilityTracker
# fmt: off
container[GroupChatOrchestration] = lambda c: GroupChatOrchestration(
    manager=container[GroupChatManager],
    agent_response_callback=c[SimpleObservabilityTracker].agent_response_callback,  # pyright: ignore[reportArgumentType]
    members=[
        container[ContentWriterChatCompletionAgent],
        container[ContentReviewerChatCompletionAgent],
        # c[BlogPostsMCPChatCompletionAgent],   # TODO? or XXX? the 2 other agents are VERY chatty
    ])
# fmt: on

# fmt: off
container[GroupChatBuiltinOrchestrationInvoker] = lambda c: GroupChatBuiltinOrchestrationInvoker(
    logger=container[Logger],
    runtime=container[InProcessRuntime],
    orchestration=c[GroupChatOrchestration])
# fmt: on


# fmt: off
container[HandoffOrchestration] = lambda c: HandoffOrchestration(
    agent_response_callback=c[FunctionObservabilityTracker].agent_response_callback,  # pyright: ignore[reportArgumentType]
    human_response_function=c[InputHumanResponse].human_response_function,
    handoffs=container[OrchestrationHandoffs],
    members=[
        container[TriageChatCompletionAgent],
        container[BasicChatCompletionAgent],
        container[LightChatCompletionAgent],
        container[MathChatCompletionAgent]])
# fmt: on


# fmt: off
container[HandoffBuiltinOrchestrationInvoker] = lambda c: HandoffBuiltinOrchestrationInvoker(
    logger=container[Logger],
    runtime=container[InProcessRuntime],
    orchestration=c[HandoffOrchestration])
# fmt: on


container[LightCustomSemanticA2AgentInvoker] = lambda c: LightCustomSemanticA2AgentInvoker(
    config=c[Config],
    kernel=createKernel(c, [c[LightPlugin]]),
    chat_history=createChatHistory(c, system_message=c[LightChatCompletionAgent].instructions),
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
)


container[DemoStdioMCPCustomSemanticA2Agent] = lambda c: DemoStdioMCPCustomSemanticA2Agent(
    config=c[Config],
    kernel=createKernel(c, [c[DemoStdioMCPPlugin]]),
    chat_history=createChatHistory(c, system_message=c[DemoMCPChatCompletionAgent].instructions),
    chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
)


# The main (and only) agent
container[SemanticA2AInvokerProtocol] = lambda c: c[LightCustomSemanticA2AgentInvoker]
container[AgentExecutor] = lambda c: A2AgentInvokerExecutor(agent=c[SemanticA2AInvokerProtocol])

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
    agent_card=c[SemanticA2AInvokerProtocol].agent_card,
    extended_agent_card=c[SemanticA2AInvokerProtocol].extended_agent_card)
# fmt: on


container[Starlette] = lambda c: c[A2AStarletteApplication].build()  # type: ignore  # FIXME
