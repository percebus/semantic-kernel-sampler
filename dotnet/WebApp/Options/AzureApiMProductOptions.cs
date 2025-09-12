namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using System.ComponentModel.DataAnnotations;

    public class AzureApiMProductOptions
    {
        [Required(ErrorMessage = ErrorMessages.SubscriptionIdRequired)]
        public string SubscriptionId { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ResourceGroupNameRequired)]
        public string ResourceGroupName { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ServiceNameRequired)]
        public string ServiceName { get; set; } = null!;

        [Required(ErrorMessage = ErrorMessages.ProductIdRequired)]
        public string ProductId { get; set; } = null!;

        public static class ErrorMessages
        {
            public const string SubscriptionIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(SubscriptionId)} cannot be empty";

            public const string ResourceGroupNameRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ResourceGroupName)} cannot be empty";

            public const string ServiceNameRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ServiceName)} cannot be empty";

            public const string ProductIdRequired = $"{AppSettingsOptions.Key}:{nameof(AiModelOptions)}:{nameof(ProductId)} cannot be empty";
        }
    }
}
