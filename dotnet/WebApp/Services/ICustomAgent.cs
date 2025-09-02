namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface ICustomAgent : IBuiltInAgent
    {
        public Task<KernelContent> InvokeAsync(KernelContent userMessage);
    }
}
