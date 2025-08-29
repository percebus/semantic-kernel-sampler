namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.ChatCompletion;

    public class MessagesController(ILogger<MessagesController> logger, Kernel kernel, ChatHistory chatHistory, IChatCompletionService chatCompletionService) : ObservableControllerBase(logger)
    {
        private Kernel Kernel { get; set; } = kernel;

        private ChatHistory ChatHistory { get; set; } = chatHistory;

        private IChatCompletionService ChatCompletionService => this.Kernel.GetService<IChatCompletionService>();

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            this.ChatHistory.AddUserMessage(request.Message);

            await

            var response = new Response
            {
                Request = request,
                Message = "Times are tough",
            };

            var result = this.Ok(response);
            return await Task.FromResult(result);
        }
    }
}
