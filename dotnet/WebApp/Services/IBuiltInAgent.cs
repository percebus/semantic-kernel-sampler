namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Agents;

    public interface IBuiltInAgent
    {
        public IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
            ICollection<ChatMessageContent> messages,
            AgentThread? thread = null,
            AgentInvokeOptions? options = null,
            CancellationToken cancellationToken = default);
    }
}
