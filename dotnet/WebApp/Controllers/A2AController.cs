namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A;
    using Microsoft.AspNetCore.Mvc;

    public class A2AController(ILogger<A2AController> logger, HttpClient httpClient) : ObservableControllerBase(logger)
    {
        private readonly HttpClient httpClient = httpClient;

        [HttpGet("agent-card")]
        public async Task<IActionResult> GetAgentCardAsync()
        {
            try
            {
                this.Logger.LogInformation("Fetching agent card from remote A2A service");

                using var response = await this.httpClient.GetAsync("http://localhost:8082/.well-known/agent-card.json");

                if (!response.IsSuccessStatusCode)
                {
                    this.Logger.LogWarning("Failed to fetch agent card: {StatusCode}", response.StatusCode);
                    return this.StatusCode((int)response.StatusCode, "Failed to fetch agent card from remote service");
                }

                var agentCard = await response.Content.ReadFromJsonAsync<AgentCard>();

                if (agentCard == null)
                {
                    this.Logger.LogWarning("Received null agent card from remote service");
                    return this.StatusCode(500, "Invalid agent card received from remote service");
                }

                this.Logger.LogInformation("Successfully retrieved agent card: {AgentName}", agentCard.Name);
                return this.Ok(agentCard);
            }
            catch (HttpRequestException ex)
            {
                this.Logger.LogError(ex, "HTTP error while fetching agent card");
                return this.StatusCode(503, "Remote A2A service unavailable");
            }
            catch (Exception ex)
            {
                this.Logger.LogError(ex, "Error fetching agent card from remote A2A service");
                return this.StatusCode(500, "Internal server error");
            }
        }
    }
}