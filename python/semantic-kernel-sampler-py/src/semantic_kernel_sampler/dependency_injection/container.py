from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.os_environ.azure_openai import AzureOpenAISettings
from semantic_kernel_sampler.configuration.os_environ.settings import Settings
from semantic_kernel_sampler.configuration.os_environ.utils import load_dotenv_files
from semantic_kernel_sampler.plugins.light import LightPlugin
from semantic_kernel_sampler.plugins.math import MathPlugin

# from semantic_kernel.functions import KernelArguments  # TODO?
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


def create_azure_prompt_execution_settings(c: ReadableContainer) -> AzureChatPromptExecutionSettings:
    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = c[FunctionChoiceBehavior]
    return settings


def create_kernel(c: ReadableContainer) -> Kernel:
    kernel = Kernel()

    plugins = c[list[PluginProtocol]]
    for plugin in plugins:
        kernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    return kernel


container = Container()

load_dotenv_files()
container[Config] = Singleton(Config())
container[Settings] = lambda c: c[Config].settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai

container[MathPlugin] = lambda c: MathPlugin()
container[LightPlugin] = lambda c: LightPlugin()
container[list[PluginProtocol]] = lambda c: [c[MathPlugin], c[LightPlugin]]

container[ChatHistory] = lambda c: ChatHistory()

container[FunctionChoiceBehavior] = lambda c: FunctionChoiceBehavior.Auto()  # type: ignore
container[AzureChatPromptExecutionSettings] = Singleton(AzureChatPromptExecutionSettings)

container[AzureChatCompletion] = lambda c: AzureChatCompletion(**c[AzureOpenAISettings])  # type: ignore

container[Kernel] = create_kernel
