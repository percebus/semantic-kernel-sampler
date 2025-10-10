from typing import Protocol

from agent_framework import ChatMessage, Workflow, WorkflowRunResult


class WorkflowRunnerProtocol(Protocol):
    workflow: Workflow

    async def run_async(self, messages: list[ChatMessage]) -> WorkflowRunResult: ...
