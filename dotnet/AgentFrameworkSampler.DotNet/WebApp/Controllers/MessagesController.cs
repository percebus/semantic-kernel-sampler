namespace JCystems.AgentFraweworkSampler.DotNet.WebApp.Controllers
{
    using System.Text.RegularExpressions;
    using JCystems.AgentFrameworkSampler.DotNet.Shared.Factories;
    using JCystems.AgentFraweworkSampler.DotNet.WebApp.Models;
    using Microsoft.Agents.AI;
    using Microsoft.AspNetCore.Mvc;

    public class MessagesController : ObservableControllerBase
    {
        private IA2AgentOrchestratorFactory AgentFactory { get; }

        private Lazy<Task<AIAgent>> AIAgent { get; }

        public MessagesController(ILogger<MessagesController> logger, IA2AgentOrchestratorFactory agentFactory)
            : base(logger)
        {
            this.AgentFactory = agentFactory;
            this.AIAgent = new Lazy<Task<AIAgent>>(async () => await this.AgentFactory.CreateAIAgentAsync());
        }

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
                AIAgent oAIAgent = await this.AIAgent.Value;
                await foreach (AgentRunResponseUpdate oAgentRunResponseUpdate in oAIAgent.RunStreamingAsync(request.Message))
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
