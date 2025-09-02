namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel.ChatCompletion;

    public interface IBuiltinAgent
    {
        public Task<ChatMessageContentItemCollection> InvokeAsync(ChatMessageContentItemCollection messages);
    }
}
