namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Factories
{
    using System.Threading.Tasks;
    using Microsoft.Agents.AI;
    using Microsoft.Agents.AI.Workflows;

    public interface IA2AgentOrchestratorFactory
    {
        Task<AIAgent> CreateAIAgentAsync();

        Task<Workflow> CreateWorkflowAsync();
    }
}
