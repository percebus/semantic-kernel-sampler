namespace JCystems.AgentFraweworkSampler.DotNet.WebApp.Models
{
    public class Request
    {
        public Guid Id { get; set; } = Guid.NewGuid();

        public required string Message { get; set; }
    }
}
