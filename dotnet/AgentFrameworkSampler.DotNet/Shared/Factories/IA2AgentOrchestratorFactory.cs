namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Factories
{
    using System.Threading.Tasks;
    using Microsoft.Agents.AI;

    public interface IA2AgentOrchestratorFactory
    {
        Task<AIAgent> CreateAIAgentAsync();
    }
}