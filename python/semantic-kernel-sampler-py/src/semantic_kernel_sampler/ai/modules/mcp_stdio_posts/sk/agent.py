from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class DemoStdioMCPBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):

    description: Optional[str] = field(default="An agent that interfaces with an MCP server with tools like 'greeting resource', and 'Add 2 numbers'.")
