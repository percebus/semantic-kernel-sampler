namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Options
{
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Connectors.OpenAI;

    public class PromptOptions
    {
        public const string Key = "PromptOptions";

        public PromptExecutionSettings? PromptExecutionSettings { get; set; } = null;

        public OpenAIPromptExecutionSettings OpenAIPromptExecutionSettings { get; set; } = new OpenAIPromptExecutionSettings
        {
            ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions,
        };

        public static class ErrorMessages
        {
        }
    }
}
