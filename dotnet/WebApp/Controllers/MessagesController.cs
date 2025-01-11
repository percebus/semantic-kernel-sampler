namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Models;
    using Microsoft.AspNetCore.Mvc;

    public class MessagesController : ObservableControllerBase
    {
        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
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
