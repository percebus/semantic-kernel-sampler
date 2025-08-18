from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from a2a.types import AgentCard
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.a2a.agents.protocol import AgentProtocol
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel

if TYPE_CHECKING:
    from semantic_kernel.contents.chat_message_content import ChatMessageContent


@dataclass
class SemanticChatAgentBase(ABC, AgentProtocol):

    config: Config = field()

    kernel: Kernel = field()

    chat_history: ChatHistory = field()

    chat_completion: ChatCompletionClientBase = field()

    prompt_execution_settings: PromptExecutionSettings = field()

    _system_message: str = field(init=False)

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(init=False, default=None)

    def __post_init__(self):
        if self._system_message:
            self.chat_history.add_system_message(self._system_message)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        self.chat_history.add_user_message(request.message)

        oResponse: ResponseModel = ResponseModel(request=request)

        # fmt: off
        oChatMessageContent: Optional[ChatMessageContent] = await self.chat_completion.get_chat_message_content(
            kernel=self.kernel,
            settings=self.prompt_execution_settings,
            chat_history=self.chat_history)
        # fmt: on

        if oChatMessageContent:
            oResponse.message = str(oChatMessageContent)
            self.chat_history.add_assistant_message(oResponse.message)

        return oResponse
