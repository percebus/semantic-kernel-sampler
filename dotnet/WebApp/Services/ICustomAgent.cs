namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface ICustomAgent
    {
        public Task<ChatMessageContent> InvokeAsync(string userMessage);
    }
}
