FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
WORKDIR /src
COPY . .
RUN ls -la


FROM base AS project
ARG DOTNET_CONFIGURATION=Release
ARG DOTNET_PROJECTS="./SemanticKernelSampler.DotNet.sln"
ARG DOTNET_TEST_FILTER="TestCategory!=Integration & TestCategory!=Flaky"
RUN dotnet restore $DOTNET_PROJECTS


FROM project AS built
RUN dotnet build $DOTNET_PROJECTS --configuration $DOTNET_CONFIGURATION -o /app/build


FROM built AS tested
RUN dotnet test $DOTNET_PROJECTS --filter "$DOTNET_TEST_FILTER"


FROM project AS published
RUN dotnet publish ./WebApp/SemanticKernelSampler.Dotnet.WebApp.csproj --configuration $DOTNET_CONFIGURATION --property:PublishDir=/app/publish


FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS webapp
USER app
WORKDIR /app
COPY --from=published /app/publish .
RUN ls -la
EXPOSE 8080
EXPOSE 8081
ENTRYPOINT ["dotnet", "JCystems.SemanticKernelSampler.Dotnet.WebApp.dll"]
