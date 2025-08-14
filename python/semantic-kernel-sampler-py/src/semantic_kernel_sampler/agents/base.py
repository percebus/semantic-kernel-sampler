from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.agents.protocol import AgentProtocol
from semantic_kernel_sampler.plugins.protocol import PluginProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel

if TYPE_CHECKING:
    from semantic_kernel.contents.chat_message_content import ChatMessageContent


@dataclass
class SemanticAgentBase(AgentProtocol, ABC):
    kernel: Kernel = field()

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError


@dataclass
class ChatSemanticAgentBase(SemanticAgentBase, ABC):
    kernel: Kernel = field()

    system_prompt: str = field()

    chat_history: ChatHistory = field()

    azure_chat_completion: AzureChatCompletion = field()

    prompt_execution_settings: PromptExecutionSettings = field()

    plugins: list[PluginProtocol] = field(default_factory=list)  # type: ignore # FIXME

    def __post_init__(self):
        self.prompt_execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()  # type: ignore # XXX FIXME

        for plugin in self.plugins:
            self.kernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        self.chat_history.add_user_message(request.message)

        oResponse: ResponseModel = ResponseModel(request=request)

        # fmt: off
        oChatMessageContent: Optional[ChatMessageContent] = await self.azure_chat_completion.get_chat_message_content(
            kernel=self.kernel,
            settings=self.prompt_execution_settings,
            chat_history=self.chat_history)
        # fmt: on

        if oChatMessageContent:
            oResponse.message = str(oChatMessageContent)
            self.chat_history.add_assistant_message(oResponse.message)

        return oResponse
