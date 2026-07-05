# Architecture

    Client
      |
    FastAPI
      |
    Routes
      |
    Services
      |
    AI Provider
      |
    OpenAI / Ollama

    Routes
      |
    SQLModel
      |
    PostgreSQL

Layers: - api/: HTTP endpoints - services/: business logic - models/:
persistence - core/: infrastructure
