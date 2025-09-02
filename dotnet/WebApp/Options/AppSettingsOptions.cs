namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using System.ComponentModel.DataAnnotations;
    using Microsoft.Extensions.Options;

    public class AppSettingsOptions
    {
        public const string Key = "JCystems:SemanticKernelSampler.DotNet.WebApp";

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.PromptOptionsRequired)]
        public PromptOptions Prompt { get; set; } = new();

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.AiModelOptionsRequired)]
        public AiModelOptions AiModel { get; set; } = new();

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.CopilotStudioOptionsRequired)]
        public CopilotStudioOptions CopilotStudio { get; set; } = new();

        public static class ErrorMessages
        {
            public const string PromptOptionsRequired = $"{Key}:{nameof(Prompt)} cannot be empty";

            public const string AiModelOptionsRequired = $"{Key}:{nameof(AiModel)} cannot be empty";

            public const string CopilotStudioOptionsRequired = $"{Key}:{nameof(CopilotStudio)} cannot be empty";
        }
    }
}
