from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel.agents import ChatCompletionAgent  # pylint: disable=E0611 # no-name-in-module

from semantic_kernel_sampler.ai.tooling.light.instructions import SYSTEM_MESSAGE
from semantic_kernel_sampler.sk.agents.executors.base.semantic.chat.agent import ChatCompletionSemanticAgentExecutorBase


@dataclass
class LightAgent(ChatCompletionSemanticAgentExecutorBase):
    _instructions: Optional[str] = field(init=False, default=SYSTEM_MESSAGE)

    def __post_init__(self):
        self.agent = ChatCompletionAgent(kernel=self.kernel, name=self.__class__.__name__, instructions=self._instructions)
