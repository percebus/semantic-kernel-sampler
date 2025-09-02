namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface ICustomAgent : IBuiltinAgent
    {
        public Task<KernelContent> InvokeAsync(KernelContent userMessage);
    }
}
