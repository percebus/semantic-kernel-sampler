from dataclasses import dataclass

from semantic_kernel.agents import ChatCompletionAgent  # pylint: disable=E0611 # no-name-in-module

from semantic_kernel_sampler.ai.tooling.light.instructions import SYSTEM_MESSAGE
from semantic_kernel_sampler.sk.agents.executors.base.semantic.chat.agent import ChatCompletionSemanticAgentExecutorBase


@dataclass
class LightAgent(ChatCompletionSemanticAgentExecutorBase):
    def __post_init__(self):
        self.agent = ChatCompletionAgent(kernel=self.kernel, name=self.__class__.__name__, instructions=SYSTEM_MESSAGE)
