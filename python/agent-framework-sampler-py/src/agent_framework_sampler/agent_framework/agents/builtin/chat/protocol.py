from typing import Protocol

from agent_framework import AgentRunResponse, ChatAgent, ChatMessage


class AgentRunnerProtocol(Protocol):
    chat_agent: ChatAgent

    async def run_async(self, messages: list[ChatMessage]) -> AgentRunResponse: ...
