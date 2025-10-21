namespace JCystems.AgentFrameworkSampler.DotNet.Shared.AI.Agents
{
    using System;
    using System.Threading.Tasks;
    using A2A;
    using Microsoft.Agents.AI;
    using Microsoft.Extensions.AI;
    using Microsoft.Extensions.Logging;

    /// <summary>
    ///  
    /// </summary>
    /// <see ref="https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/A2AClient/HostClientAgent.cs"/>
    public class MultiA2AgentOrchestrator(ILogger<MultiA2AgentOrchestrator> logger, IChatClient chatClient)
    {
        public AIAgent? Agent { get; private set; }

        public ILogger<MultiA2AgentOrchestrator> Logger { get; } = logger;

        private IChatClient ChatClient { get; } = chatClient;

        private static async Task<AIAgent> CreateAgentAsync(Uri agentUri)
        {
            var oHttpClient = new HttpClient
            {
                Timeout = TimeSpan.FromSeconds(60)
            };

            var oA2ACardResolver = new A2ACardResolver(agentUri, oHttpClient);
            return await oA2ACardResolver.GetAIAgentAsync();
        }

        internal async Task InitializeAgentAsync(IEnumerable<Uri> agentUrls)
        {
            try
            {
                this.Logger.LogInformation("Initializing Agent Framework agent");

                // Connect to the remote agents via A2A
                var createAgentTasks = agentUrls.Select(CreateAgentAsync);
                var agents = await Task.WhenAll(createAgentTasks);
                var tools = agents
                        .Select(agent => (AITool)agent.AsAIFunction())
                        .ToList();

                // Create the agent that uses the remote agents as tools
                this.Agent = this.ChatClient.CreateAIAgent(
                    name: "HostClient",
                    instructions: "You specialize in handling queries for users and using your tools to provide answers.",
                    tools: tools);
            }
            catch (Exception ex)
            {
                this.Logger.LogError(ex, "Failed to initialize HostClientAgent");
                throw;
            }
        }
    }
}
