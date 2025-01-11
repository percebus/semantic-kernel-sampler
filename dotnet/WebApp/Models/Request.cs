namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Models
{
    public class Request
    {
        public required Guid Id { get; set; } = Guid.NewGuid();

        public required string Message { get; set; }
    }
}
