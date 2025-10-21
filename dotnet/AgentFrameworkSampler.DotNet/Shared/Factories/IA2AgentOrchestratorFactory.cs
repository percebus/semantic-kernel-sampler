namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Factories
{
    using System.Threading.Tasks;
    using Microsoft.Agents.AI;
    using Microsoft.Extensions.Logging;

    public interface IA2AgentOrchestratorFactory
    {
        ILogger<IA2AgentOrchestratorFactory> Logger { get; }

        Task<AIAgent> CreateAIAgentAsync();
    }
}