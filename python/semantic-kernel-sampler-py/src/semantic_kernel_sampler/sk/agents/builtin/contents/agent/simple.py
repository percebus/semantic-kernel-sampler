from dataclasses import dataclass, field
from logging import Logger

from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.agents.builtin.contents.agent.protocol import AgentResponseProtocol


@dataclass
class SimpleObservabilityTracker(AgentResponseProtocol):
    logger: Logger = field()

    def agent_response_callback(self, message: ChatMessageContent) -> None:
        """Observer function to print the messages from the agents.

        Please note that this function is called whenever the agent generates a response,
        including the internal processing messages (such as tool calls) that are not visible
        to other agents in the orchestration.
        """
        self.logger.info("%s: %s", message.name, message.content)
