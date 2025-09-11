namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A;

    /// <summary>
    /// Service for resolving A2A agent cards from remote services.
    /// </summary>
    public interface IA2ACardResolver
    {
        /// <summary>
        /// Resolves an agent card from a remote A2A service.
        /// </summary>
        /// <param name="serviceUrl">The URL of the A2A service.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The resolved agent card.</returns>
        Task<AgentCard?> ResolveAgentCardAsync(string serviceUrl, CancellationToken cancellationToken = default);
    }
}