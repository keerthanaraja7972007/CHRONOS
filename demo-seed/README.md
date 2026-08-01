# Demo seed

The executable seed module is located at `backend/demo_seed/seed.py` so it shares the application database configuration and models. It creates the `demo@chronos.dev` user, `acme/payments-api`, pull request #142, and a representative completed risk assessment.

Run it with:

```bash
cd backend
python -m demo_seed.seed
```
