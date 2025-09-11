namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using A2A;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.AspNetCore.Mvc;

    [Route("api/a2a/client")]
    public class A2AClientController(ILogger<A2AClientController> logger, IA2AService a2aService) : ObservableControllerBase(logger)
    {
        [HttpGet("agent-card")]
        public async Task<IActionResult> GetAgentCardAsync()
        {
            if (a2aService.Card is null)
            {
                await a2aService.InitializeAsync();
            }

            if (a2aService.Card is null)
            {
                throw new Exception("Something went wrong, could not fetch Agent Card!");
            }

            try
            {
                this.Logger.LogInformation("Fetching agent card from remote A2A service using A2ACardResolver");

                AgentCard oAgentCard = a2aService.Card;
                this.Logger.LogInformation("Successfully retrieved agent card: {AgentName}", oAgentCard.Name);
                return this.Ok(oAgentCard);
            }
            catch (Exception ex)
            {
                this.Logger.LogError(ex, "Error fetching agent card from remote A2A service");
                return this.StatusCode(500, "Internal server error");
            }
        }
    }
}
