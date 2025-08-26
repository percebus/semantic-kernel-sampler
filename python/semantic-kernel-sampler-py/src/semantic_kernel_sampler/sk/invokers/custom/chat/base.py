from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.kernel_content import KernelContent

from semantic_kernel_sampler.sk.invokers.protocol import InvokerProtocol

if TYPE_CHECKING:
    from semantic_kernel.contents.chat_message_content import ChatMessageContent


@dataclass
class CustomSemanticChatInvokerBase(ABC, InvokerProtocol[KernelContent]):
    kernel: Kernel = field()

    chat_history: ChatHistory = field()

    chat_completion: ChatCompletionClientBase = field()

    prompt_execution_settings: PromptExecutionSettings = field()

    async def invoke(self, messages: list[KernelContent]) -> Optional[KernelContent]:
        # FIXME HACK
        first_message: KernelContent = messages[0]
        message_text: str = str(first_message)

        self.chat_history.add_user_message(message_text)

        # fmt: off
        responseChatMessageContent: Optional[ChatMessageContent] = await self.chat_completion.get_chat_message_content(
            kernel=self.kernel,
            settings=self.prompt_execution_settings,
            chat_history=self.chat_history)
        # fmt: on

        if responseChatMessageContent:
            response_text: str = str(responseChatMessageContent)
            self.chat_history.add_assistant_message(response_text)

        return responseChatMessageContent
