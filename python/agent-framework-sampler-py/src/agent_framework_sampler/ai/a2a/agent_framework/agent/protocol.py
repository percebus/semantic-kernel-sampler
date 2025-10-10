from agent_framework_sampler.a2a.cards.protocol import A2ACardsProtocol
from agent_framework_sampler.agent_framework.agents.builtin.chat.runner.protocol import ChatAgentRunnerProtocol


class A2AgentFrameworkRunnerProtocol(A2ACardsProtocol, ChatAgentRunnerProtocol):
    # NOTE: Inherited
    # agent_card: AgentCard
    # extended_agent_card: Optional[AgentCard]

    # NOTE: Inherited
    # async def run_async(self, messages: list[ChatMessage]) -> AgentRunResponse: ...
    ...
