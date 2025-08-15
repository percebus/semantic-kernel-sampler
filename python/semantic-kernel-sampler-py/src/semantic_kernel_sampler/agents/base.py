from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Optional

from a2a.types import AgentCard
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.agents.protocol import AgentProtocol
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.plugins.protocol import PluginProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel

if TYPE_CHECKING:
    from semantic_kernel.contents.chat_message_content import ChatMessageContent


@dataclass
class AgentBase(ABC, AgentProtocol):
    config: Config = field()

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError


@dataclass
class SemanticAgentBase(ABC, AgentProtocol):
    config: Config = field()

    kernel: Kernel = field()

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(init=False, default=None)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError


@dataclass
class SemanticChatAgentBase(ABC, AgentProtocol):
    plugins: ClassVar[list[PluginProtocol]] = []

    config: Config = field()

    kernel: Kernel = field()

    chat_history: ChatHistory = field()

    azure_chat_completion: AzureChatCompletion = field()

    prompt_execution_settings: PromptExecutionSettings = field()

    system_message: str = field(init=False)

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(init=False, default=None)

    def __post_init__(self):
        if self.system_message:
            self.chat_history.add_system_message(self.system_message)

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
