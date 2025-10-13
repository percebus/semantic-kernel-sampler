namespace JCystems.AgentFrameworkSampler.Dotnet.Shared.Options
{
    using System.ComponentModel.DataAnnotations;

    public class AzureCredentialOptions
    {
        [Required(ErrorMessage = ErrorMessages.TenantIdRequired)]
        public string TenantId { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ClientIdRequired)]
        public string ClientId { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ClientSecretRequired)]
        public string ClientSecret { get; set; } = null!;

        public static class ErrorMessages
        {
            public const string TenantIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(TenantId)} cannot be empty";

            public const string ClientIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ClientId)} cannot be empty";

            public const string ClientSecretRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ClientSecret)} cannot be empty";
        }
    }
}
