from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel.agents import ChatCompletionAgent  # pylint: disable=no-name-in-module

from semantic_kernel_sampler.ai.modules.mcp_stdio_demo.instructions.v1 import INSTRUCTIONS
from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.base import ChatCompletionBuiltinAgentInvokerBase


@dataclass
class MCPDemoBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvokerBase):
    _instructions: Optional[str] = field(default=INSTRUCTIONS)

    def __post_init__(self):
        self.agent = ChatCompletionAgent(kernel=self.kernel, name=self.__class__.__name__, instructions=self._instructions)
