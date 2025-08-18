

from dataclasses import dataclass, field

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent

from semantic_kernel_sampler.ai.tooling.light.sk.kernel import LightKernel
from semantic_kernel_sampler.sk.agents.executors.base.semantic.chat.agent import ChatCompletionSemanticAgentExecutorBase


@dataclass
class LightAgent(ChatCompletionSemanticAgentExecutorBase):

    kernel: Kernel = field(default_factory=LightKernel)

    def __post_init__(self):
        self.agent = ChatCompletionAgent(
            kernel=self.kernel,
            name=self.__class__.__name__,
            instructions="You are a helpful assistant."
        )
