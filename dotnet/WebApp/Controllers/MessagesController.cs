namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Agents;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class MessagesController(ILogger<MessagesController> logger, Agent agent) : ObservableControllerBase(logger)
    {
        private Agent Agent => agent;

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            this.Logger.LogInformation("Received request: {Request}", request);
            var requestChatMessageContent = new ChatMessageContent(AuthorRole.User, request.Message);
            var requestMessages = new List<ChatMessageContent> { requestChatMessageContent };

            AgentThread? thread = null;
            await foreach (AgentResponseItem<ChatMessageContent> item in this.Agent.InvokeAsync(requestMessages, thread))
            {
                thread = item.Thread;
                this.Logger.LogInformation("Request message content item: {Item}", item);

                ChatMessageContent responseChatMessageContent = item.Message;
                var response = new Response
                {
                    Request = request,
                    Message = responseChatMessageContent.Content,
                };

                this.Logger.LogInformation("Sending response: {Response}", response);
                var result = this.Ok(response);
                return await Task.FromResult(result);
            }

            throw new Exception("No response received");
        }
    }
}
