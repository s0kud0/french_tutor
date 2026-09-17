# Development Guide

## Normal workflow

1.  Edit in VS Code.
2.  Run with Docker Compose.
3.  Test via /docs or curl.
4.  Update documentation.

## Frontend workflow

1.  Start the complete production-style stack with Docker Compose. The app is
    available at http://localhost/ and the API docs at http://localhost/docs.
2.  In a second terminal, run:

    ``` bash
    cd frontend
    npm install
    npm run dev
    ```

3.  For live frontend iteration, start the local-development overlay first:

    ``` bash
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d api
    ```

4.  Open the Vite URL shown in the terminal. Vite proxies API routes to the
    locally exposed API on port 8000. The overlay is for development only and
    is not used by the homelab deployment.

## Project layout

api/app is the Python application root.

Avoid bypassing the provider abstraction when adding AI features.
