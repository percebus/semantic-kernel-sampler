namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.AspNetCore.Mvc;

    public class A2AController(ILogger<A2AController> logger, IA2ACardResolver a2aCardResolver) : ObservableControllerBase(logger)
    {
        private readonly IA2ACardResolver a2aCardResolver = a2aCardResolver;

        [HttpGet("agent-card")]
        public async Task<IActionResult> GetAgentCardAsync()
        {
            try
            {
                this.Logger.LogInformation("Fetching agent card from remote A2A service using A2ACardResolver");

                var agentCard = await this.a2aCardResolver.ResolveAgentCardAsync("http://localhost:8082");

                if (agentCard == null)
                {
                    this.Logger.LogWarning("Failed to resolve agent card from remote A2A service");
                    return this.StatusCode(503, "Remote A2A service unavailable or returned invalid data");
                }

                this.Logger.LogInformation("Successfully retrieved agent card: {AgentName}", agentCard.Name);
                return this.Ok(agentCard);
            }
            catch (Exception ex)
            {
                this.Logger.LogError(ex, "Error fetching agent card from remote A2A service");
                return this.StatusCode(500, "Internal server error");
            }
        }
    }
}