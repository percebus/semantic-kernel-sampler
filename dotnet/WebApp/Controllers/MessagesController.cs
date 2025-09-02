namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class MessagesController(ILogger<MessagesController> logger, ICustomAgent agent) : ObservableControllerBase(logger)
    {
        private IBuiltInAgent Agent => agent;

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            this.Logger.LogInformation("Received request: {Request}", request);
            var requestChatMessageContent = new ChatMessageContent(AuthorRole.User, request.Message);
            var requestMessages = new ChatMessageContentItemCollection { requestChatMessageContent };
            IReadOnlyList<KernelContent> replyMessages = await this.Agent.InvokeAsync(requestMessages);
            KernelContent firstReplyChatMessageContent = replyMessages[0];

            var response = new Response
            {
                Request = request,
                Message = firstReplyChatMessageContent.ToString(),
            };

            this.Logger.LogInformation("Sending response: {Response}", response);
            var result = this.Ok(response);
            return await Task.FromResult(result);
        }
    }
}
