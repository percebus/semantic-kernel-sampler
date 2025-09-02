namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface ICustomAgent : IBuiltIn_Agent
    {
        public Task<KernelContent> InvokeAsync(KernelContent userMessage);
    }
}
