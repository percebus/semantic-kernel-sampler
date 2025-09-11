namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A
{
    public class AgentSkill
    {
        public required string Id { get; set; }

        public required string Name { get; set; }

        public required string Description { get; set; }

        public List<string> Tags { get; set; } = new List<string>();

        public List<string> Examples { get; set; } = new List<string>();
    }
}