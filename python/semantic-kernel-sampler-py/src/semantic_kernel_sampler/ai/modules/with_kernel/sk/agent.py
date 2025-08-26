from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel.agents import ChatCompletionAgent  # pylint: disable=no-name-in-module

from semantic_kernel_sampler.ai.modules.with_kernel.instructions.v1 import INSTRUCTIONS
from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class AssistantAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    _instructions: Optional[str] = field(init=False, default=INSTRUCTIONS)

    def __post_init__(self):
        self.agent = ChatCompletionAgent(kernel=self.kernel, name="Assistant", instructions=self._instructions)
