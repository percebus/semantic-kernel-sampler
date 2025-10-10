from dataclasses import dataclass, field
from typing import Optional

from agent_framework import AgentRunResponse, AgentThread, ChatAgent, ChatMessage

from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.protocol import ChatAgentRunnerProtocol


@dataclass
class ThreadedChatAgentRunner(ChatAgentRunnerProtocol):
    chat_agent: ChatAgent = field()

    service_thread_id: Optional[str] = field(default=None)

    agent_thread: AgentThread = field(init=False)

    def __post_init__(self) -> None:
        self.agent_thread = self.chat_agent.get_new_thread(service_thread_id=self.service_thread_id)

    async def run_async(self, messages: list[ChatMessage]) -> AgentRunResponse:
        return await self.chat_agent.run(messages, thread=self.agent_thread)
