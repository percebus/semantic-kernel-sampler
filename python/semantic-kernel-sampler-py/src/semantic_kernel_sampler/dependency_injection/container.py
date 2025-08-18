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

from semantic_kernel_sampler.a2a.agents.light import LightAgent
from semantic_kernel_sampler.a2a.agents.math import MathAgent
from semantic_kernel_sampler.a2a.agents.protocol import AgentProtocol
from semantic_kernel_sampler.a2a.agents.typescript_sdk__quick_start import DemoMcpServerAgent
from semantic_kernel_sampler.a2a.executor import MyAgentExecutor
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.logs import LoggingConfig
from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.sk.plugins.light import LightPlugin
from semantic_kernel_sampler.sk.plugins.math import MathPlugin

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel_sampler.sk.plugins.mcp.typescript_sdk__quick_start import DemoServerMCPStdioPlugin
from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


def createKernel(c: ReadableContainer) -> Kernel:
    oKernel = Kernel()

    oChatCompletion = c[ChatCompletionClientBase]
    oKernel.add_service(oChatCompletion)

    # XXX Troubleshooting
    # NOTE: Plugins are set on each Agent now
    # plugins = c[list[PluginProtocol]]
    # for plugin in plugins:
    #     oKernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    return oKernel


def createChatHistory(c: ReadableContainer) -> ChatHistory:
    oChatHistory = ChatHistory()

    # XXX Troubleshooting
    # oChatHistory.add_system_message("""You are a helpful assistant.
    #     You will only use the registered plugin(s).
    #     If it's not in the plugins, say 'I cannot help with that.'""")

    return oChatHistory


container = Container()

load_dotenv_files()  # TODO move to a __main__.py?
# TODO? Remove all default_factory and initialize here?
container[Config] = Singleton(Config())
container[LoggingConfig] = lambda c: c[Config].logging

container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai
container[A2ASettings] = lambda c: c[Settings].a2a

container[MathPlugin] = MathPlugin
container[LightPlugin] = LightPlugin
container[DemoServerMCPStdioPlugin] = DemoServerMCPStdioPlugin

# NOTE: Plugins to register in the Kernel
# fmt: off
container[list[PluginProtocol]] = lambda c: [
    c[MathPlugin],
    c[LightPlugin],
    c[DemoServerMCPStdioPlugin]
]
# fmt: on

container[ChatHistory] = createChatHistory

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

container[Kernel] = createKernel

# fmt: off
container[LightAgent] = lambda c: LightAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oLightPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on

# fmt: off
container[MathAgent] = lambda c: MathAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    chat_completion=c[ChatCompletionClientBase],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oMathPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on


# fmt: off
container[DemoMcpServerAgent] = lambda c: DemoMcpServerAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oMathPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on


# The main (and only) agent
container[AgentProtocol] = lambda c: c[LightAgent]
container[AgentExecutor] = lambda c: MyAgentExecutor(agent=c[AgentProtocol])

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
    agent_card=c[AgentProtocol].agent_card,
    extended_agent_card=c[AgentProtocol].extended_agent_card)
# fmt: on


container[Starlette] = lambda c: c[A2AStarletteApplication].build()  # type: ignore  # FIXME
