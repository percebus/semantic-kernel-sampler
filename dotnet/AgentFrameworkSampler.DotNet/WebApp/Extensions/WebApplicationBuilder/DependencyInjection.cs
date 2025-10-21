namespace JCystems.AgentFraweworkSampler.DotNet.WebApp.Extensions.WebApplicationBuilder
{
    using System.ClientModel;
    using System.Diagnostics.CodeAnalysis;
    using System.Text.Json;
    using A2A;
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Core;
    using Azure.Identity;
    using JCystems.AgentFrameworkSampler.DotNet.Shared.Options;
    using Microsoft.AspNetCore.Http.Json;
    using Microsoft.Extensions.AI;
    using Microsoft.Extensions.DependencyInjection.Extensions;
    using Microsoft.Extensions.Options;
    using OpenAI.Chat;
    using Scrutor;
    using Serilog;
    using JokerChatClientAgent = Microsoft.Agents.AI.ChatClientAgent;


    [ExcludeFromCodeCoverage]
    public static class DependencyInjection
    {
        public static Microsoft.AspNetCore.Builder.WebApplicationBuilder RegisterServices(this Microsoft.AspNetCore.Builder.WebApplicationBuilder builder)
        {
            builder.Configuration.AddJsonFile("appsettings.json", optional: false);
            builder.Configuration.AddJsonFile("appsettings.ai.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.env.json", optional: true, reloadOnChange: true);
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

            builder.Services.TryAddSingleton<AzureCliCredential>();
            builder.Services.TryAddSingleton<VisualStudioCredential>();

            builder.Services.TryAddSingleton<DefaultAzureCredential>(provider => new(
                new DefaultAzureCredentialOptions()
                {
                    // Exclude credentials that often fail with CA policies
                    // ExcludeSharedTokenCacheCredential = true, // XXX OBSOLETE
                    ExcludeInteractiveBrowserCredential = true,
                    ExcludeAzurePowerShellCredential = true,

                    // Keep these for development
                    ExcludeAzureCliCredential = false,
                    ExcludeVisualStudioCredential = true,
                    ExcludeVisualStudioCodeCredential = true,
                    ExcludeManagedIdentityCredential = true,
                }));

            builder.Services.TryAddSingleton<ClientSecretCredential>(provider =>
            {
                AzureCredentialOptions oAzureCredentialOptions = appSettings.AzureCredential;
                return new(
                    oAzureCredentialOptions.TenantId,
                    oAzureCredentialOptions.ClientId,
                    oAzureCredentialOptions.ClientSecret);
            });

            builder.Services.TryAddSingleton<TokenCredential>(provider =>
            {
                // NOTE: Choose either or
                return provider.GetRequiredService<AzureCliCredential>();
                // return provider.GetRequiredService<VisualStudioCredential>();
                // return provider.GetRequiredService<DefaultAzureCredential>();
                // return provider.GetRequiredService<ClientSecretCredential>();
            });


            builder.Services.TryAddSingleton<ApiKeyCredential>(provider => new AzureKeyCredential(appSettings.AiModel.ApiKey));
            builder.Services.TryAddScoped<AzureOpenAIClient>(provider =>
            {
                var oApiKeyCredential = provider.GetRequiredService<ApiKeyCredential>();
                return new(appSettings.AiModel.Endpoint, oApiKeyCredential);
            });

            builder.Services.AddTransient<ChatClient>(provider => provider
                .GetRequiredService<AzureOpenAIClient>()
                .GetChatClient(appSettings.AiModel.DeploymentId));

            builder.Services.AddTransient<IChatClient>(provider => provider
                .GetRequiredService<ChatClient>()
                .AsIChatClient());

            // SRC: https://github.com/microsoft/semantic-kernel/blob/main/dotnet/samples/GettingStartedWithAgents/A2A/Step01_A2AAgent.cs
            builder.Services.TryAddTransient<HttpClientHandler>();
            // builder.Services.TryAddTransient<LoggingHandler>(); // FIXME
            builder.Services.TryAddScoped<HttpClient>(provider =>
            {
                var oHttpClientFactory = provider.GetRequiredService<IHttpClientFactory>();
                // var oLoggingHandler = provider.GetRequiredService<LoggingHandler>(); // FIXME
                return oHttpClientFactory.CreateClient();
            });

            builder.Services.TryAddScoped<IEnumerable<A2ACardResolver>>(provider =>
            {
                return appSettings.A2A.AgentsUris.Select(agentUri =>
                {
                    // TODO? use IHttpClientFactory?
                    var oHttpClient = new HttpClient
                    {
                        Timeout = TimeSpan.FromSeconds(60),
                    };

                    return new A2ACardResolver(agentUri, oHttpClient);
                });
            });

            // SRC: https://github.com/microsoft/agent-framework/blob/dotnet-1.0.0-preview.251009.1/dotnet/samples/GettingStarted/Agents/Agent_Step01_Running/Program.cs
            builder.Services.TryAddScoped<JokerChatClientAgent>(provider => provider
                .GetRequiredService<IChatClient>()
                .CreateAIAgent(name: "Joker", instructions: "You are good at telling jokes."));

            builder.Services.Scan(
                s => s.FromAssemblyOf<Program>()
                      .AddClasses()
                      .UsingRegistrationStrategy(RegistrationStrategy.Skip)
                      .AsMatchingInterface());

            builder.Services.Scan(
                s => s.FromAssemblyOf<AppSettingsOptions>()
                      .AddClasses()
                      .UsingRegistrationStrategy(RegistrationStrategy.Skip)
                      .AsMatchingInterface());

            // Add services to the container.
            builder.Services.AddControllers();

            // Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
            builder.Services.AddOpenApi();
            builder.Services.AddOpenApiDocument();

            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddHealthChecks();

            // Add HTTP client for A2A communication
            builder.Services.AddHttpClient();

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
