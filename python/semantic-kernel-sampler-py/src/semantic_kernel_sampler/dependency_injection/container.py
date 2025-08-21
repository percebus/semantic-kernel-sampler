from logging import Logger
from typing import Optional

from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.tasks.task_store import TaskStore
from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from starlette.applications import Starlette

from semantic_kernel_sampler.a2a.agents.protocol import A2AgentProtocol
from semantic_kernel_sampler.a2a.executor import A2AgentExecutor
from semantic_kernel_sampler.ai.modules.light.agent import LightAgent
from semantic_kernel_sampler.ai.modules.light.instructions.v1 import INSTRUCTIONS as light_instructions
from semantic_kernel_sampler.ai.modules.light.sk.agent_executor import LightSemanticAgentExecutor
from semantic_kernel_sampler.ai.modules.light.sk.plugin.v1 import LightPlugin
from semantic_kernel_sampler.ai.modules.math.agent import MathAgent
from semantic_kernel_sampler.ai.modules.math.instructions.v1 import INSTRUCTIONS as math_instructions
from semantic_kernel_sampler.ai.modules.math.sk.plugin.v1 import MathPlugin
from semantic_kernel_sampler.ai.modules.mcp_stdio_demo.agent import DemoMcpServerAgent
from semantic_kernel_sampler.ai.modules.mcp_stdio_demo.instructions.v1 import INSTRUCTIONS as mcp_instructions

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel_sampler.ai.modules.mcp_stdio_demo.sk.agent_executor import MCPDemoSemanticAgentExecutor
from semantic_kernel_sampler.ai.modules.mcp_stdio_demo.sk.plugin import DemoStdIOMCPPlugin
from semantic_kernel_sampler.ai.modules.with_kernel.sk.agent import AssistantAgentExecutor as AssistantChatCompletionAgentExecutor
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.logs import LoggingConfig
from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


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
container[DemoStdIOMCPPlugin] = lambda c: DemoStdIOMCPPlugin(logger=c[Logger])

# NOTE: If you need all Plugins for w/e reason
# fmt: off
container[list[PluginProtocol]] = lambda c: [
    c[MathPlugin],
    c[LightPlugin],
    c[DemoStdIOMCPPlugin]]
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

container[AssistantChatCompletionAgentExecutor] = lambda c: AssistantChatCompletionAgentExecutor(
    kernel=createKernel(c),
)

container[LightSemanticAgentExecutor] = lambda c: LightSemanticAgentExecutor(
    kernel=createKernel(c, [c[LightPlugin]]),
)

container[MCPDemoSemanticAgentExecutor] = lambda c: MCPDemoSemanticAgentExecutor(
    kernel=createKernel(c, [c[DemoStdIOMCPPlugin]]),
)

# fmt: off
container[LightAgent] = lambda c: LightAgent(
    config=c[Config],
    kernel=createKernel(c, [c[LightPlugin]]),
    chat_history=createChatHistory(c, system_message=light_instructions),
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
)
# fmt: on

# fmt: off
container[MathAgent] = lambda c: MathAgent(
    config=c[Config],
    kernel=createKernel(c, [c[MathPlugin]]),
    chat_history=createChatHistory(c, system_message=math_instructions),
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
)
# fmt: on


# fmt: off
container[DemoMcpServerAgent] = lambda c: DemoMcpServerAgent(
    config=c[Config],
    kernel=createKernel(c, [c[DemoStdIOMCPPlugin]]),
    chat_history=createChatHistory(c, system_message=mcp_instructions),
    chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
)
# fmt: on


# The main (and only) agent
container[A2AgentProtocol] = lambda c: c[LightAgent]
container[AgentExecutor] = lambda c: A2AgentExecutor(agent=c[A2AgentProtocol])

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
    agent_card=c[A2AgentProtocol].agent_card,
    extended_agent_card=c[A2AgentProtocol].extended_agent_card)
# fmt: on


container[Starlette] = lambda c: c[A2AStarletteApplication].build()  # type: ignore  # FIXME
