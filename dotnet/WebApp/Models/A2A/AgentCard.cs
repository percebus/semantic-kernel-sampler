namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Models.A2A
{
    public class AgentCard
    {
        public required string Name { get; set; }

        public required string Description { get; set; }

        public required string Url { get; set; }

        public required string Version { get; set; }

        public List<string> DefaultInputModes { get; set; } = new List<string>();

        public List<string> DefaultOutputModes { get; set; } = new List<string>();

        public AgentCapabilities? Capabilities { get; set; }

        public bool SupportsAuthenticatedExtendedCard { get; set; } = false;

        public List<AgentSkill> Skills { get; set; } = new List<AgentSkill>();
    }
}