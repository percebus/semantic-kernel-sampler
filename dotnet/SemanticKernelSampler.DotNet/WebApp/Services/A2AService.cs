namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using System.Net.Http;
    using A2A;
    using Microsoft.SemanticKernel.Agents.A2A;

    public class A2AService(HttpClient httpClient, Uri baseURI) : IA2AService
    {
        public A2ACardResolver CardResolver { get; } = new A2ACardResolver(baseURI, httpClient);

        public AgentCard? Card { get; private set; } = null;

        public A2AClient Client { get; } = new A2AClient(baseURI, httpClient);

        public A2AAgent? Agent { get; private set; } = null;

        public async Task InitializeAsync()
        {
            this.Card = await this.CardResolver.GetAgentCardAsync();
            this.Agent = new A2AAgent(this.Client, this.Card);
        }
    }
}
