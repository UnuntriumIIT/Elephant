#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:5.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["Elephant/Elephant.csproj", "Elephant/"]
RUN dotnet restore "Elephant/Elephant.csproj"
COPY . .
WORKDIR "/src/Elephant"
RUN dotnet build "Elephant.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Elephant.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Elephant.dll"]