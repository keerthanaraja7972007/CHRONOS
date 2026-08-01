# Deployment

## Offline demo

Copy `.env.example` to `.env`, then run `docker compose up --build`. Open `http://localhost:5173`, select **Try demo mode**, and run any seeded pull request. No external credential or network service is required after dependencies/images have been installed.

## Production

Set `ENVIRONMENT=production`, a strong `SECRET_KEY`, managed PostgreSQL `DATABASE_URL`, restrictive `CORS_ORIGINS`, and disable `ENABLE_DEMO_AUTH`. Apply migrations with `alembic upgrade head` before launching the API. Configure GitHub OAuth only when connecting live repositories.

## Troubleshooting

- `503 Demo data is not initialized`: run the seed module or restart the backend container.
- Database connection error: verify `DATABASE_URL` and PostgreSQL health.
- Frontend API errors: ensure the API is running on port 8000 and Vite/nginx proxy is configured.
