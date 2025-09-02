namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Services
{
    using System.Runtime.CompilerServices;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Agents;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class CustomChatAgent(ILogger<ICustomChatAgent> logger, IChatCompletionService chatCompletionService, ChatHistory chatHistory) : ICustomChatAgent
    {
        private ILogger<ICustomChatAgent> Logger => logger;

        // TODO? public?
        private ChatHistory ChatHistory => chatHistory;

        // TODO? public?
        private IChatCompletionService ChatCompletionService => chatCompletionService;

        public async Task<ChatMessageContent> InvokeAsync(ChatMessageContent userMessage)
        {
            this.Logger.LogInformation("Invoking CustomChatAgent with user message: {userMessage}", userMessage);

            string? userMessageContent = userMessage.Content;
            if (string.IsNullOrEmpty(userMessageContent))
            {
                throw new ArgumentException("User message content cannot be null or empty.", nameof(userMessage));
            }

            this.ChatHistory.AddUserMessage(userMessageContent);

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/ChatCompletion/AzureOpenAI_ChatCompletion.cs
            ChatMessageContent replyChatMessageContent = await this.ChatCompletionService.GetChatMessageContentAsync(this.ChatHistory);
            this.Logger.LogInformation("Received reply from ChatCompletionService: {reply}", replyChatMessageContent.Content);
            this.ChatHistory.Add(replyChatMessageContent);

            this.Logger.LogInformation("CustomChatAgent received reply message: {firstReplyMessage}", replyChatMessageContent);

            return replyChatMessageContent;
        }


        public async IAsyncEnumerable<AgentResponseItem<ChatMessageContent>> InvokeAsync(
            ICollection<ChatMessageContent> messages,
            AgentThread? thread = null,
            AgentInvokeOptions? options = null,
            [EnumeratorCancellation] CancellationToken cancellationToken = default)
        {
            ChatMessageContent firstRequestMessage = messages.First();
            ChatMessageContent replyMessage = await this.InvokeAsync(firstRequestMessage);

            if (thread is null)
            {
                throw new ArgumentNullException(nameof(thread), "AgentThread cannot be null.");
            }

            yield return new AgentResponseItem<ChatMessageContent>(replyMessage, thread);
        }
    }
}
