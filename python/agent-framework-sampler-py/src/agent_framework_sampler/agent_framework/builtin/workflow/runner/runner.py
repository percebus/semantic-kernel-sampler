from dataclasses import dataclass, field

from agent_framework import ChatMessage, Workflow, WorkflowRunResult

from agent_framework_sampler.agent_framework.builtin.workflow.runner.protocol import WorkflowRunnerProtocol


@dataclass
class WorkflowRunner(WorkflowRunnerProtocol):
    workflow: Workflow = field()

    async def run_async(self, messages: list[ChatMessage]) -> WorkflowRunResult:
        if not self.workflow:
            raise ValueError("Workflow not initialized.")

        oWorkflowRunResult: WorkflowRunResult = await self.workflow.run(messages)
        return oWorkflowRunResult
