# Development

## Backend

Create a virtual environment, install `backend/requirements.txt`, set `DATABASE_URL`, then run:

```bash
alembic upgrade head
python -m demo_seed.seed
uvicorn backend.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite development server proxies `/api` to port 8000.
