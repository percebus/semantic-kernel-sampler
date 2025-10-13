namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using System.ComponentModel.DataAnnotations;
    using Microsoft.SemanticKernel;

    public class PromptOptions
    {
        public const string Key = "PromptOptions";

        // Auto-invoke Plugins
        [Required]
        public FunctionChoiceBehavior FunctionChoiceBehavior { get; set; } = FunctionChoiceBehavior.Auto();

        public static class ErrorMessages
        {
        }
    }
}
