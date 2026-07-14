# Development Guide

## Normal workflow

1.  Edit in VS Code.
2.  Run with Docker Compose.
3.  Test via /docs or curl.
4.  Update documentation.

## Frontend workflow

1.  Start the backend with Docker Compose.
2.  In a second terminal, run:

    ``` bash
    cd frontend
    npm install
    npm run dev
    ```

3.  Open the Vite URL shown in the terminal.

## Project layout

api/app is the Python application root.

Avoid bypassing the provider abstraction when adding AI features.
