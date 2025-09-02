namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface IBuiltInAgent
    {
        public Task<IReadOnlyList<KernelContent>> InvokeAsync(IReadOnlyList<KernelContent> messages);
    }
}
