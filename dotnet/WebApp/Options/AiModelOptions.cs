namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using System.ComponentModel.DataAnnotations;

    public class AiModelOptions
    {
        [Required(ErrorMessage = ErrorMessages.EndpointRequired)]
        public Uri Endpoint { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.DeploymentIdRequired)]
        public string DeploymentId { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ModelIdRequired)]
        public string ModelId { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ApiVersionRequired)]
        public string ApiVersion { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ApiKeyRequired)]
        public string ApiKey { get; set; } = null!;

        public static class ErrorMessages
        {
            public const string EndpointRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(Endpoint)} cannot be empty";

            // TODO
            //public const string EndpointHttpSchemaRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(Endpoint)} field is not a valid HTTP/HTTPS URI.";

            public const string DeploymentIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(DeploymentId)} cannot be empty";

            public const string ModelIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ModelId)} cannot be empty";

            public const string ApiVersionRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ApiVersion)} cannot be empty";

            public const string ApiKeyRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ApiKey)} cannot be empty";
        }
    }
}
