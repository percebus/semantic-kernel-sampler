namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using System.Threading.Tasks;
    using A2A;
    using Microsoft.SemanticKernel.Agents.A2A;

    public interface IA2AService
    {
        A2ACardResolver CardResolver { get; }

        AgentCard? Card { get; }

        A2AClient Client { get; }

        A2AAgent? Agent { get; }

        Task InitializeAsync();
    }
}
