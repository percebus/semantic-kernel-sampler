namespace JCystems.AgentFraweworkSampler.DotNet.WebApp.Controllers
{
    using System.Text.RegularExpressions;
    using JCystems.AgentFrameworkSampler.DotNet.Shared.Factories;
    using JCystems.AgentFraweworkSampler.DotNet.WebApp.Models;
    using Microsoft.Agents.AI.Workflows;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.AI;

    public class MessagesController : ObservableControllerBase
    {
        private IA2AgentOrchestratorFactory AgentFactory { get; }

        private Lazy<Task<Workflow>> Workflow { get; }

        public MessagesController(ILogger<MessagesController> logger, IA2AgentOrchestratorFactory agentFactory)
            : base(logger)
        {
            this.AgentFactory = agentFactory;
            this.Workflow = new Lazy<Task<Workflow>>(async () => await this.AgentFactory.CreateWorkflowAsync());
        }

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody] Request request, CancellationToken cancellationToken)
        {
            this.Logger.LogInformation("Received request: {Request}", request);

            if (string.IsNullOrWhiteSpace(request.Message))
            {
                return this.StatusCode(400, "Request.Message is required");
            }

            var response = new Response
            {
                Request = request,
            };

            List<ChatMessage> messages = new();
            try
            {
                Workflow oWorkflow = await this.Workflow.Value;
                ChatMessage requestChatMessage = new ChatMessage(ChatRole.User, request.Message);
                List<ChatMessage> requestChatMessages = new List<ChatMessage> { requestChatMessage };
                await using StreamingRun oStreamingResult = await InProcessExecution.StreamAsync(oWorkflow, requestChatMessages, cancellationToken: cancellationToken);
                TurnToken oTurnToken = new(emitEvents: true);
                await oStreamingResult.TrySendMessageAsync(oTurnToken);
                await foreach (WorkflowEvent oWorkflowEvent in oStreamingResult.WatchStreamAsync())
                {
                    this.Logger.LogDebug("WorkflowEvent: {oWorkflowEvent}", oWorkflowEvent);
                    switch (oWorkflowEvent)
                    {
                        case WorkflowOutputEvent oWorkflowOutputEvent:
                            this.Logger.LogInformation("WorkflowOutputEvent: {oWorkflowOutputEvent}", oWorkflowOutputEvent);
                            List<ChatMessage> workflowMessages = oWorkflowOutputEvent.As<List<ChatMessage>>()!;
                            messages.AddRange(workflowMessages);
                            break;
                    }
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
                    messages
                        .Select(oAgentRunResponseUpdate => oAgentRunResponseUpdate.Text))
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
