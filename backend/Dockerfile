FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY backend /app/backend
COPY .env.example /app/.env.example
WORKDIR /app/backend
CMD ["sh", "-c", "alembic upgrade head && python -m demo_seed.seed && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
