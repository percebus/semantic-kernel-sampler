namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Extensions.WebApplicationBuilder
{
    using System.ClientModel;
    using System.Diagnostics.CodeAnalysis;
    using System.Text.Json;
    using Azure;
    using Azure.AI.OpenAI;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Options;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.Agents.CopilotStudio.Client;
    using Microsoft.AspNetCore.Http.Json;
    using Microsoft.Extensions.AI;
    using Microsoft.Extensions.DependencyInjection.Extensions;
    using Microsoft.Extensions.Options;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Agents.Copilot;
    using Microsoft.SemanticKernel.ChatCompletion;
    using Scrutor;
    using Serilog;

    [ExcludeFromCodeCoverage]
    public static class DependencyInjection
    {
        public static Microsoft.AspNetCore.Builder.WebApplicationBuilder RegisterServices(this Microsoft.AspNetCore.Builder.WebApplicationBuilder builder)
        {
            builder.Configuration.AddJsonFile("appsettings.json", optional: false);
            builder.Configuration.AddJsonFile("appsettings.ai.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.copilotstudio.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true);
            builder.Configuration.AddEnvironmentVariables();

            builder.Services.AddOptions<AppSettingsOptions>()
                .BindConfiguration(AppSettingsOptions.Key)
                .ValidateDataAnnotations()
                .ValidateOnStart();

            var provider = builder.Services.BuildServiceProvider();

            ILogger logger = Log.ForContext<Program>();

            AppSettingsOptions appSettings;
            try
            {
                // this gets us a copy of appSettings to use at startup
                appSettings = provider.GetRequiredService<IOptionsMonitor<AppSettingsOptions>>().CurrentValue;
            }
            catch (Exception ex)
            {
                logger.Fatal(ex, "Invalid configuration, please verify that your configuration is correct. Error: {ex}", ex.Message);
                throw;
            }

            builder.Services.TryAddSingleton<FunctionChoiceBehavior>(FunctionChoiceBehavior.Auto());
            builder.Services.TryAddSingleton<PromptExecutionSettings>(provider =>
            {
                var oFunctionChoiceBehavior = provider.GetRequiredService<FunctionChoiceBehavior>();
                return new()
                {
                    FunctionChoiceBehavior = oFunctionChoiceBehavior,
                };
            });

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/Agents/ChatCompletion_ServiceSelection.cs
            builder.Services.TryAddScoped<ApiKeyCredential>(provider => new AzureKeyCredential(appSettings.AiModel.ApiKey));
            builder.Services.TryAddScoped<AzureOpenAIClient>(provider =>
            {
                var oApiKeyCredential = provider.GetRequiredService<ApiKeyCredential>();
                return new(appSettings.AiModel.Endpoint, oApiKeyCredential);
            });

            builder.Services.TryAddScoped<ChatHistory>(provider =>
            {
                // TODO: Add System Message
                return new();
            });

            // TODO? or XXX?
            // builder.Services.AddTransient<IChatClient>(provider =>
            // {
            //     var oAzureOpenAIClient = provider.GetRequiredService<AzureOpenAIClient>();
            //     return oAzureOpenAIClient.GetChatClient(appSettings.AiModel.DeploymentId).AsIChatClient();
            // });

            builder.Services.TryAddTransient<IKernelBuilder>(provider => Kernel.CreateBuilder());

            builder.Services.TryAddTransient<Kernel>(provider =>
            {
                var oKernelBuilder = provider.GetRequiredService<IKernelBuilder>();
                var oAzureOpenAIClient = provider.GetRequiredService<AzureOpenAIClient>();

                // NOTE: Chose 1 or the other?
                // oKernelBuilder.AddAzureOpenAIChatClient(appSettings.AiModel.DeploymentId, oAzureOpenAIClient);
                oKernelBuilder.AddAzureOpenAIChatCompletion(appSettings.AiModel.DeploymentId, oAzureOpenAIClient);

                // oKernelBuilder.Plugins.AddFromType<YourTypeHere>(); // TODO: Add your plugins here

                return oKernelBuilder.Build();
            });

            builder.Services.TryAddScoped<IChatCompletionService>(provider =>
            {
                var oKernel = provider.GetRequiredService<Kernel>();
                return oKernel.GetRequiredService<IChatCompletionService>();
            });

#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
            builder.Services.TryAddSingleton<CopilotStudioConnectionSettings>(provider => new(
                appSettings.CopilotStudio.TenantId,
                appSettings.CopilotStudio.ClientId,
                appSettings.CopilotStudio.ClientSecret));

            builder.Services.TryAddScoped<CopilotClient>(provider =>
            {
                var oCopilotStudioConnectionSettings = provider.GetRequiredService<CopilotStudioConnectionSettings>();
                return CopilotStudioAgent.CreateClient(oCopilotStudioConnectionSettings);
            });

            builder.Services.TryAddTransient<CopilotStudioAgent>(provider =>
            {
                var oCopilotClient = provider.GetRequiredService<CopilotClient>();
                return new(oCopilotClient);
            });
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

            builder.Services.Scan(
                s => s.FromAssemblyOf<Program>()
                      .AddClasses()
                      .UsingRegistrationStrategy(RegistrationStrategy.Skip)
                      .AsMatchingInterface());

            builder.Services.TryAddScoped<ICustomAgent, CustomChatAgent>();

            // Add services to the container.
            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            builder.Services.AddHealthChecks();

            // TODO: Add resiliency
            // builder.Services.ConfigureHttpClientDefaults(http =>
            // {
            //     // Turn on resilience by default
            //     http.AddStandardResilienceHandler();
            // });

            builder.Services.Configure<JsonOptions>(oJsonOptions =>
            {
                JsonSerializerOptions oJsonSerializerOptions = oJsonOptions.SerializerOptions;
                oJsonSerializerOptions.PropertyNameCaseInsensitive = false;
                oJsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            });

            return builder;
        }
    }
}
