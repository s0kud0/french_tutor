# Project Context

This document is the living source of truth.

## Current Runtime

-   Docker Compose is the canonical runtime.
-   FastAPI + PostgreSQL + Redis.

## AI

Routes -\> services -\> provider.py -\> concrete provider.

Current provider: - OpenAI

Planned: - Ollama

## Principles

-   Thin routes
-   Business logic in services
-   Configuration in core
-   SQLModel for persistence
