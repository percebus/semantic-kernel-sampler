namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Factories
{
    using System;
    using System.Threading.Tasks;
    using A2A;
    using Microsoft.Agents.AI;
    using Microsoft.Extensions.AI;
    using Microsoft.Extensions.Logging;

    /// <summary>A2 Agent Orchestrator Factory.</summary>
    /// <see ref="https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/A2AClient/HostClientAgent.cs"/>
    public class A2AgentOrchestratorFactory(ILogger<A2AgentOrchestratorFactory> logger, IChatClient chatClient, IEnumerable<A2ACardResolver> a2aCardResolvers) : IA2AgentOrchestratorFactory
    {
        private ILogger<A2AgentOrchestratorFactory> Logger { get; } = logger;

        private IChatClient ChatClient { get; } = chatClient;

        private IEnumerable<A2ACardResolver> A2ACardResolvers { get; } = a2aCardResolvers;

        public async Task<AIAgent> CreateAIAgentAsync()
        {
            this.Logger.LogInformation("Creating Agent Framework agent");

            AIAgent[] agents = await this.CreateA2AgentsAsAsync();
            IList<AITool> tools = agents
                    .Select(agent => (AITool)agent.AsAIFunction())
                    .ToList();

            // Create the agent that uses the remote agents as tools
            return this.ChatClient.CreateAIAgent(
                name: "HostClient",
                instructions: "You specialize in handling queries for users and using your tools to provide answers.",
                tools: tools);
        }

        private async Task<AIAgent[]> CreateA2AgentsAsAsync()
        {
            // Connect to the remote agents via A2A
            IEnumerable<Task<AIAgent>> createAgentTasks = this.A2ACardResolvers
                .Select(async oA2ACardResolver => await oA2ACardResolver.GetAIAgentAsync());

            return await Task.WhenAll(createAgentTasks);
        }
    }
}
