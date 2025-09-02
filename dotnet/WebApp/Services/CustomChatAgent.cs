namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class CustomChatAgent(ILogger<ICustomChatAgent> logger, IChatCompletionService chatCompletionService, ChatHistory chatHistory) : ICustomChatAgent
    {
        private ILogger<ICustomChatAgent> Logger => logger;

        // TODO? public?
        private ChatHistory ChatHistory => chatHistory;

        // TODO? public?
        private IChatCompletionService ChatCompletionService => chatCompletionService;

        public async Task<ChatMessageContent> InvokeAsync(string userMessage)
        {
            this.Logger.LogInformation("Invoking CustomChatAgent with user message: {userMessage}", userMessage);

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/ChatCompletion/AzureOpenAI_ChatCompletion.cs
            this.ChatHistory.AddUserMessage(userMessage);

            ChatMessageContent replyChatMessageContent = await this.ChatCompletionService.GetChatMessageContentAsync(this.ChatHistory);
            this.Logger.LogInformation("Received reply from ChatCompletionService: {reply}", replyChatMessageContent.Content);

            this.ChatHistory.Add(replyChatMessageContent);
            return replyChatMessageContent;
        }
    }
}
