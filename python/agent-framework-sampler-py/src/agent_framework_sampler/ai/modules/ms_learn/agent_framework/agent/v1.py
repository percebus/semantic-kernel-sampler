from dataclasses import dataclass, field

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol

from agent_framework_sampler.ai.modules.ms_learn.agent_framework.tools.ms_learn import MSLearnMCPStreamableHttpTool


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/tools/ai_tool_with_approval.py
@dataclass
class MSLearnChatAgent(ChatAgent):
    chat_client: ChatClientProtocol = field()

    ms_learn_tool: MSLearnMCPStreamableHttpTool = field()

    instructions: str = field(default=("You are a helpful assistant. Use the MCP tool."))

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
            tools=[self.ms_learn_tool],
        )
