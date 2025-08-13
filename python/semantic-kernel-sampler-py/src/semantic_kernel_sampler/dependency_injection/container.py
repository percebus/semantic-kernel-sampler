from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.plugins.light import LightPlugin
from semantic_kernel_sampler.plugins.math import MathPlugin

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


def createKernel(c: ReadableContainer) -> Kernel:
    oKernel = Kernel()

    plugins = c[list[PluginProtocol]]
    for plugin in plugins:
        oKernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    oAzureChatCompletion = c[AzureChatCompletion]
    oKernel.add_service(oAzureChatCompletion)

    return oKernel


def createChatHistory(c: ReadableContainer) -> ChatHistory:
    oChatHistory = ChatHistory()

    # TODO Read from file
    msg = """
        You are a helpful assistant.
        You will only use the registered plugins.
        If it's not in the plugins, say 'I cannot help with that.'"
    """

    oChatHistory.add_system_message(msg)
    return oChatHistory


container = Container()

load_dotenv_files()  # TODO move to a __main__.py?

container[Config] = Singleton(Config())
container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai

container[MathPlugin] = MathPlugin
container[LightPlugin] = LightPlugin
container[list[PluginProtocol]] = lambda c: [c[MathPlugin], c[LightPlugin]]

container[ChatHistory] = createChatHistory

container[FunctionChoiceBehavior] = Singleton(FunctionChoiceBehavior.Auto)  # type: ignore  # FIXME?
container[PromptExecutionSettings] = lambda c: AzureChatPromptExecutionSettings(function_choice_behavior=c[FunctionChoiceBehavior])

container[AzureChatCompletion] = lambda c: AzureChatCompletion(
    base_url=c[AzureOpenAISettings].base_url,
    api_key=c[AzureOpenAISettings].api_key,
    deployment_name=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
)

container[Kernel] = createKernel
