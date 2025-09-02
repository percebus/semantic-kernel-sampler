namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.SemanticKernel;

    public class MessagesController(ILogger<MessagesController> logger, ICustomAgent agent) : ObservableControllerBase(logger)
    {
        private ICustomAgent Agent => agent;

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            ChatMessageContent replyChatMessageContent = await this.Agent.InvokeAsync(request.Message);

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
