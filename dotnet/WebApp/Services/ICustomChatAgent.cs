namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface ICustomChatAgent : IBuiltInAgent
    {
        public Task<ChatMessageContent> InvokeAsync(ChatMessageContent userMessage);
    }
}
