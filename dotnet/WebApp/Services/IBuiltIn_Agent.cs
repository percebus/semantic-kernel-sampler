namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;

    public interface IBuiltIn_Agent
    {
        public Task<IReadOnlyList<KernelContent>> InvokeAsync(IReadOnlyList<KernelContent> messages);
    }
}
