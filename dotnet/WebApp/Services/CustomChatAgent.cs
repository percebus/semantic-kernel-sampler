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

            var requestMessages = new ChatMessageContentItemCollection { userMessage };
            ChatMessageContentItemCollection replyMessages = await this.InvokeAsync(requestMessages);

            KernelContent firstReplyMessage = replyMessages[0];
            this.Logger.LogInformation("CustomChatAgent received reply message: {firstReplyMessage}", firstReplyMessage);

            return firstReplyMessage;
        }

        public async Task<ChatMessageContentItemCollection> InvokeAsync(ChatMessageContentItemCollection requestMessages)
        {
            this.ChatHistory.AddUserMessage(requestMessages);

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/ChatCompletion/AzureOpenAI_ChatCompletion.cs
            ChatMessageContent replyChatMessageContent = await this.ChatCompletionService.GetChatMessageContentAsync(this.ChatHistory);
            this.Logger.LogInformation("Received reply from ChatCompletionService: {reply}", replyChatMessageContent.Content);
            this.ChatHistory.Add(replyChatMessageContent);

            var replyMessages = new ChatMessageContentItemCollection { replyChatMessageContent };
            return replyMessages;
        }
    }
}
