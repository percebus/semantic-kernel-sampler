namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Options
{
    using System.ComponentModel.DataAnnotations;
    using JCystems.AgentFrameworkSampler.DotNet.Shared.Options.CustomValidationAttributes;

    public class A2AOptions
    {
        [Required(ErrorMessage = ErrorMessages.AgentsUrisRequired)]
        [NotEmptyCollection(ErrorMessage = ErrorMessages.SomeAgentUrisRequired)]
        public List<Uri> AgentsUris { get; set; } = new();

        public static class ErrorMessages
        {
            public const string AgentsUrisRequired = $"{AppSettingsOptions.Key}:{nameof(A2AOptions)}:{nameof(AgentsUris)} cannot be empty";

            public const string SomeAgentUrisRequired = $"{AppSettingsOptions.Key}:{nameof(A2AOptions)}:{nameof(AgentsUris)} must contain at least one valid URI";
        }
    }
}
