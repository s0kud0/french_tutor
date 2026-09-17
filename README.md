# French Tutor

A Docker-first French tutoring platform with a React chat interface and
FastAPI backend.

## Goals

-   Modular AI provider architecture
-   Persistent conversation history
-   Easy local development with Docker
-   Future support for OpenAI and Ollama

## Quick Start

``` bash
docker compose up --build
```

Visit:

- http://localhost/ for the chat application
- http://localhost/docs for the FastAPI documentation
- http://localhost/health for the health check

In the homelab deployment, use http://french-tutor/ instead. Docker Compose
publishes only the web container on port 80; PostgreSQL, Redis, and FastAPI
remain on the internal Compose network.

See DEVELOPMENT.md for developer workflow.
