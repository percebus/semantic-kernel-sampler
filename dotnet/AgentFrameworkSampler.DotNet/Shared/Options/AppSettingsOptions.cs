namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Options
{
    using System.ComponentModel.DataAnnotations;
    using Microsoft.Extensions.Options;

    public class AppSettingsOptions
    {
        public const string Key = "JCystems:AgentFrameworkSampler.DotNet.WebApp";

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.AzureCredentialOptionsRequired)]
        public AzureCredentialOptions AzureCredential { get; set; } = new();

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.AiModelOptionsRequired)]
        public AiModelOptions AiModel { get; set; } = new();

        [ValidateObjectMembers]
        [Required(ErrorMessage = ErrorMessages.A2AOptionsRequired)]
        public A2AOptions A2A { get; set; } = new();


        public static class ErrorMessages
        {
            public const string A2AOptionsRequired = $"{Key}:{nameof(A2AOptions)} cannot be empty";

            public const string AiModelOptionsRequired = $"{Key}:{nameof(AiModel)} cannot be empty";

            public const string AzureCredentialOptionsRequired = $"{Key}:{nameof(AzureCredential)} cannot be empty";
        }
    }
}
