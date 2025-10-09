from typing import Optional, Protocol

from agent_framework import AgentRunResponse, ChatAgent, ChatMessage


class AgentRunnerProtocol(Protocol):
    chat_agent: ChatAgent

    service_thread_id: Optional[str]

    async def run_async(self, messages: list[ChatMessage]) -> AgentRunResponse: ...
