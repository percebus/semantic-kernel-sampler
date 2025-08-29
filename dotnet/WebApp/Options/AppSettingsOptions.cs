namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    public class AppSettingsOptions
    {
        public const string Key = "JCystems:SemanticKernelSampler.DotNet.WebApp";

        public PromptOptions Prompt { get; set; } = new();

        public AiModelOptions AiModel { get; set; } = new AiModelOptions();

    }
}
