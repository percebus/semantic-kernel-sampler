from dataclasses import dataclass, field
from logging import Logger

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.sk.agents.builtin.contents.human.protocol import HumanResponseProtocol


@dataclass
class InputHumanResponse(HumanResponseProtocol):
    logger: Logger = field()

    def human_response_function(self) -> ChatMessageContent:
        user_input = input("User: ")
        self.logger.info("User: %s", user_input)
        return ChatMessageContent(role=AuthorRole.USER, content=user_input)
