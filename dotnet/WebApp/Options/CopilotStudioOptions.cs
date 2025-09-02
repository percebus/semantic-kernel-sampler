namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using System.ComponentModel.DataAnnotations;

    public class CopilotStudioOptions
    {
        [Required(ErrorMessage = ErrorMessages.TenantIdRequired)]
        public string TenantId { get; set; } = string.Empty;

        [Required(ErrorMessage = ErrorMessages.ClientIdRequired)]
        public string ClientId { get; set; } = string.Empty;

        [Required(ErrorMessage = ErrorMessages.ClientSecretRequired)]
        public string ClientSecret { get; set; } = string.Empty;

        public static class ErrorMessages
        {
            public const string TenantIdRequired = $"{AppSettingsOptions.Key}:{nameof(CopilotStudioOptions)}:{nameof(TenantId)} cannot be empty";

            public const string ClientIdRequired = $"{AppSettingsOptions.Key}:{nameof(CopilotStudioOptions)}:{nameof(ClientId)} cannot be empty";

            public const string ClientSecretRequired = $"{AppSettingsOptions.Key}:{nameof(CopilotStudioOptions)}:{nameof(ClientSecret)} cannot be empty";
        }
    }
}
