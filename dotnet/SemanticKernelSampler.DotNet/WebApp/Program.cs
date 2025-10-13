using JCystems.SemanticKernelSampler.Dotnet.WebApp.Extensions.WebApplicationBuilder;

var builder = WebApplication.CreateBuilder(args);

// NOTE: See <see cref="Extensions/WebApplicationBuilder/DependencyInjection.cs"/> for more details
builder.RegisterServices();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// TODO Move to appSettings.json
string? isDotNETRunningInContainer = Environment.GetEnvironmentVariable("DOTNET_RUNNING_IN_CONTAINER");

// Only use HTTPS redirection when not running in a container
if (string.IsNullOrEmpty(isDotNETRunningInContainer))
{
    app.UseHttpsRedirection();
}
else
{
    // Skip HTTPS redirection in containers
}

app.UseAuthorization();

app.MapControllers();

app.Run();
