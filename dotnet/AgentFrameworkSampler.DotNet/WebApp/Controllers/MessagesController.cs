namespace JCystems.AgentFrameworkSampler.Dotnet.WebApp.Controllers
{
    using System.Text.RegularExpressions;
    using JCystems.AgentFrameworkSampler.Dotnet.WebApp.Models;
    using Microsoft.Agents.AI;
    using Microsoft.AspNetCore.Mvc;

    public class MessagesController(ILogger<MessagesController> logger, AIAgent aiAgent) : AgentFrameworkSampler.Dotnet.WebApp.Controllers.ObservableControllerBase(logger)
    {
        private AIAgent AIAgent => aiAgent;

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request)
        {
            this.Logger.LogInformation("Received request: {Request}", request);

            var response = new Response
            {
                Request = request,
            };

            List<AgentRunResponseUpdate> responses = new();
            try
            {
                await foreach (AgentRunResponseUpdate oAgentRunResponseUpdate in this.AIAgent.RunStreamingAsync(request.Message))
                {
                    this.Logger.LogInformation("Request message content item: {oAgentRunResponseUpdate}", oAgentRunResponseUpdate);
                    responses.Add(oAgentRunResponseUpdate);
                }
            }
            catch (Exception ex)
            {
                this.Logger.LogError(ex, "Error processing request: {Request}", request);
                return this.StatusCode(500, "Internal server error");
            }

            string responseMessages = string
                .Join(
                    Environment.NewLine,
                    responses
                        .Select(oAgentRunResponseUpdate => oAgentRunResponseUpdate.Text)
                        .Where(c => !string.IsNullOrWhiteSpace(c)))
                .Trim();

            responseMessages = Regex.Replace(responseMessages, @"\r\n", string.Empty);
            responseMessages = Regex.Replace(responseMessages, @"\s+", " ");
            response.Message = responseMessages;

            if (string.IsNullOrWhiteSpace(response.Message))
            {
                return this.StatusCode(500, "No response");
            }

            this.Logger.LogInformation("Sending response: {Response}", response);
            var result = this.Ok(response);
            return await Task.FromResult(result);
        }
    }
}
