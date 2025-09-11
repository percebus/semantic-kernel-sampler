namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A;
    using Microsoft.SemanticKernel;

    /// <summary>
    /// Implementation of A2A agent card resolver using Semantic Kernel patterns.
    /// </summary>
    public class A2ACardResolver : IA2ACardResolver
    {
        private readonly HttpClient httpClient;
        private readonly ILogger<A2ACardResolver> logger;

        public A2ACardResolver(HttpClient httpClient, ILogger<A2ACardResolver> logger)
        {
            this.httpClient = httpClient;
            this.logger = logger;
        }

        /// <inheritdoc/>
        public async Task<AgentCard?> ResolveAgentCardAsync(string serviceUrl, CancellationToken cancellationToken = default)
        {
            try
            {
                this.logger.LogInformation("Resolving agent card from A2A service: {ServiceUrl}", serviceUrl);

                var agentCardUrl = $"{serviceUrl.TrimEnd('/')}/.well-known/agent-card.json";
                var response = await this.httpClient.GetAsync(agentCardUrl, cancellationToken);

                if (!response.IsSuccessStatusCode)
                {
                    this.logger.LogWarning("Failed to resolve agent card from {Url}: {StatusCode}", agentCardUrl, response.StatusCode);
                    return null;
                }

                var agentCard = await response.Content.ReadFromJsonAsync<AgentCard>(cancellationToken: cancellationToken);

                if (agentCard != null)
                {
                    this.logger.LogInformation("Successfully resolved agent card: {AgentName} from {ServiceUrl}", agentCard.Name, serviceUrl);
                }
                else
                {
                    this.logger.LogWarning("Received null agent card from {ServiceUrl}", serviceUrl);
                }

                return agentCard;
            }
            catch (Exception ex)
            {
                this.logger.LogError(ex, "Error resolving agent card from {ServiceUrl}", serviceUrl);
                return null;
            }
        }
    }
}