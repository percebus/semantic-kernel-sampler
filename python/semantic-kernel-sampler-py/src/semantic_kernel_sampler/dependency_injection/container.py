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
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from starlette.applications import Starlette

from semantic_kernel_sampler.agent_executor import MyAgentExecutor
from semantic_kernel_sampler.agents.light import LightAgent
from semantic_kernel_sampler.agents.math import MathAgent
from semantic_kernel_sampler.agents.protocol import AgentProtocol
from semantic_kernel_sampler.agents.typescript_sdk__quick_start import TypescriptSDKQuickStartDemoServerAgent
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.plugins.light import LightPlugin
from semantic_kernel_sampler.plugins.math import MathPlugin

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel_sampler.plugins.mcp.typescript_sdk__quick_start import DemoServerMCPStdioPlugin
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


def createKernel(c: ReadableContainer) -> Kernel:
    oKernel = Kernel()

    # NOTE: Plugins will be set on each Agent now
    # plugins = c[list[PluginProtocol]]
    # for plugin in plugins:
    #     oKernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    oAzureChatCompletion = c[AzureChatCompletion]
    oKernel.add_service(oAzureChatCompletion)

    return oKernel


def createChatHistory(c: ReadableContainer) -> ChatHistory:
    oChatHistory = ChatHistory()

    # NOTE: Moved inside each Agent
    # oChatHistory.add_system_message("You are a helpful assistant.")

    return oChatHistory


container = Container()

load_dotenv_files()  # TODO move to a __main__.py?
# TODO? Remove all default_factory and initialize here?
container[Config] = Singleton(Config())
container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai
container[A2ASettings] = lambda c: c[Settings].a2a

container[MathPlugin] = MathPlugin
container[LightPlugin] = LightPlugin
container[DemoServerMCPStdioPlugin] = DemoServerMCPStdioPlugin

# fmt: off
container[list[PluginProtocol]] = lambda c: [
    c[MathPlugin],
    c[LightPlugin],
    c[DemoServerMCPStdioPlugin]]
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

container[Kernel] = createKernel

# fmt: off
container[LightAgent] = lambda c: LightAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    azure_chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oLightPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on

# fmt: off
container[MathAgent] = lambda c: MathAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    azure_chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oMathPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on


# fmt: off
container[TypescriptSDKQuickStartDemoServerAgent] = lambda c: TypescriptSDKQuickStartDemoServerAgent(
    config=c[Config],
    kernel=c[Kernel],
    chat_history=c[ChatHistory],
    azure_chat_completion=c[AzureChatCompletion],
    prompt_execution_settings=c[PromptExecutionSettings],
    # plugins=list[oMathPlugin]  # pyright: ignore[reportArgumentType]  # TODO? or XXX?
)
# fmt: on


# The main (and only) agent
container[AgentProtocol] = lambda c: c[TypescriptSDKQuickStartDemoServerAgent]
container[AgentExecutor] = lambda c: MyAgentExecutor(agent=c[TypescriptSDKQuickStartDemoServerAgent])

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
