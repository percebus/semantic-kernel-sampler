namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class MessagesController(ILogger<MessagesController> logger, Kernel kernel, ChatHistory chatHistory) : ObservableControllerBase(logger)
    {
        private Kernel Kernel { get; set; } = kernel;

        // TODO wrap in a provider
        private ChatHistory ChatHistory { get; set; } = chatHistory;

        private IChatCompletionService ChatCompletionService => this.Kernel.GetRequiredService<IChatCompletionService>();

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/ChatCompletion/AzureOpenAI_ChatCompletion.cs
            this.ChatHistory.AddUserMessage(request.Message);

            ChatMessageContent replyChatMessageContent = await this.ChatCompletionService.GetChatMessageContentAsync(this.ChatHistory);
            this.ChatHistory.Add(replyChatMessageContent);

            var response = new Response
            {
                Request = request,
                Message = replyChatMessageContent.Content,
            };

            var result = this.Ok(response);
            return await Task.FromResult(result);
        }
    }
}
