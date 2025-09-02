namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface IBuiltInAgent
    {
        // TODO REFACTOR: See below
        public Task<IReadOnlyList<KernelContent>> InvokeAsync(IReadOnlyList<KernelContent> messages);

        // public abstract IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
        //     ICollection<ChatMessageContent> messages,
        //     AgentThread? thread = null,
        //     AgentInvokeOptions? options = null,
        //     CancellationToken cancellationToken = default);
    }
}
