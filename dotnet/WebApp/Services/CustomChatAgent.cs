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

        public async Task<KernelContent> InvokeAsync(KernelContent userMessage)
        {
            this.Logger.LogInformation("Invoking CustomChatAgent with user message: {userMessage}", userMessage);

            string userMessageString = userMessage.ToString() ?? string.Empty;
            this.ChatHistory.AddUserMessage(userMessageString);

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/ChatCompletion/AzureOpenAI_ChatCompletion.cs
            ChatMessageContent replyChatMessageContent = await this.ChatCompletionService.GetChatMessageContentAsync(this.ChatHistory);
            this.Logger.LogInformation("Received reply from ChatCompletionService: {reply}", replyChatMessageContent.Content);
            this.ChatHistory.Add(replyChatMessageContent);

            this.Logger.LogInformation("CustomChatAgent received reply message: {firstReplyMessage}", replyChatMessageContent);

            return replyChatMessageContent;
        }

        public async Task<IReadOnlyList<KernelContent>> InvokeAsync(IReadOnlyList<KernelContent> requestMessages)
        {
            ChatMessageContent firstRequestMessage = (ChatMessageContent)requestMessages[0];
            KernelContent replyMessage = await this.InvokeAsync(firstRequestMessage);
            var replyMessages = new ChatMessageContentItemCollection { replyMessage };
            return replyMessages;
        }
    }
}
