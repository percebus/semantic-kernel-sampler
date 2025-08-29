namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    public class AiModelOptions
    {
        public Uri Endpoint { get; set; } = null!;

        public string DeploymentId { get; set; } = null!;

        public string ModelId { get; set; } = null!;

        public static class ErrorMessages
        {
            public const string EndpointRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(Endpoint)} cannot be empty";

            public const string DeploymentIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(DeploymentId)} cannot be empty";

            public const string ModelIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ModelId)} cannot be empty";

            public const string HttpSchemaRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(Endpoint)} field is not a valid HTTP/HTTPS URI.";
        }
    }
}
