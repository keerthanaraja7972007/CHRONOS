from __future__ import annotations
from datetime import date
from backend.incidents.models import IncidentRecord
def repository_files()->dict[str,str]:
    files={
      "services/auth/src/token.py":"from shared.config import settings\ndef issue_token(user_id): return settings.secret\n",
      "services/cart/src/cart_service.py":"from shared.cache import cache\ndef get_cart(user_id): return cache.get(user_id)\n",
      "services/payments/src/retry.py":"from shared.queue import publish\ndef retry_payment(payment): publish('payments.retry', payment)\n",
      "services/orders/src/order_service.py":"from services.payments.src.retry import retry_payment\ndef confirm(order): return retry_payment(order.payment)\n",
      "services/inventory/src/reservation.py":"def reserve(sku, quantity): return True\n",
      "services/notifications/src/sender.py":"def send(event): return event\n",
      "services/shipping/src/fulfillment.py":"def quote(address): return 0\n",
      "shared/cache.py":"def get(key): return None\n", "shared/queue.py":"def publish(topic, payload): return None\n", "shared/config.py":"class Settings: secret='demo'\nsettings=Settings()\n",
      "frontend/src/checkout.tsx":"export const Checkout = () => null;\n", "infra/kubernetes/payments.yaml":"apiVersion: apps/v1\n", "docs/architecture.md":"# Checkout architecture\n", "pyproject.toml":"[project]\nname='checkout-platform'\n"}
    components=["api","models","repository","service","handlers","validators","events","tests","config","metrics","client","schemas"]
    services=["auth","cart","payments","orders","inventory","notifications","shipping"]
    for service in services:
        for component in components:
            path=f"services/{service}/src/{component}.py"
            files.setdefault(path,f'"""{service} {component} component."""\nfrom shared.config import settings\n')
    return files
def incidents()->list[IncidentRecord]:
    data=[("database-timeout","Database timeout during checkout","Connection pool starvation","high","services/orders/src/repository.py","orders"),("authentication-regression","Authentication regression","Token validation accepted expired sessions","critical","services/auth/src/token.py","auth"),("redis-outage","Redis outage lost carts","Cache fallback was not enabled","high","services/cart/src/cart_service.py","cart"),("n-plus-one-query","N+1 query on order history","Unbounded per-order loading","medium","services/orders/src/order_service.py","orders"),("memory-leak","Notification worker memory leak","Message payloads retained after send","high","services/notifications/src/sender.py","notifications"),("cache-inconsistency","Inventory cache inconsistency","Reservation invalidation raced with checkout","high","services/inventory/src/reservation.py","inventory"),("api-rate-limit","Provider API rate limit","Shipping quote client did not back off","medium","services/shipping/src/fulfillment.py","shipping"),("queue-failure","Message queue delivery failure","Payment retry events were not durable","critical","shared/queue.py","payments"),("payment-retry-loop","Payment retry loop","Retry handler republished terminal failures","critical","services/payments/src/retry.py","payments"),("dependency-timeout","Service dependency timeout","Order confirmation waited indefinitely on payment","high","services/orders/src/order_service.py","orders")]
    return [IncidentRecord(id=id,repository="acme/checkout-service",title=title,root_cause=cause,affected_files=[file],affected_services=[service],severity=severity,occurred_on=date(2025,1,index+1),resolution="Added bounded retries, observability, and a verified rollback runbook.",tags=[service,"reliability"],content=f"{title}. Root cause: {cause}. Affected file: {file}.") for index,(id,title,cause,severity,file,service) in enumerate(data)]
def pull_requests()->list[dict]:
    return [
      {
        "number": 101,
        "risk": "low",
        "title": "Clarify checkout documentation",
        "author": "maya",
        "status": "open",
        "files_changed": ["docs/architecture.md"],
        "date": "2026-07-12T09:24:00Z",
        "description": "Clarifies the checkout architecture documentation for on-call engineers and reviewers.",
        "short_description": "Documentation-only change that updates the system overview.",
        "diff": "diff --git a/docs/architecture.md b/docs/architecture.md\n--- a/docs/architecture.md\n+++ b/docs/architecture.md\n@@ -1 +1 @@\n-# Checkout architecture\n+# Checkout service architecture\n",
      },
      {
        "number": 102,
        "risk": "medium",
        "title": "Add inventory reservation validation",
        "author": "noah",
        "status": "open",
        "files_changed": ["services/inventory/src/reservation.py"],
        "date": "2026-07-14T14:10:00Z",
        "description": "Adds input validation for inventory reservations to reduce invalid checkout requests.",
        "short_description": "Input validation logic for reservation quantity handling.",
        "diff": "diff --git a/services/inventory/src/reservation.py b/services/inventory/src/reservation.py\n--- a/services/inventory/src/reservation.py\n+++ b/services/inventory/src/reservation.py\n@@ -1 +1,2 @@\n def reserve(sku, quantity): return True\n+def validate(quantity): return quantity > 0\n",
      },
      {
        "number": 103,
        "risk": "high",
        "title": "Tune payment retry scheduling",
        "author": "alex",
        "status": "open",
        "files_changed": ["services/payments/src/retry.py"],
        "date": "2026-07-18T11:32:00Z",
        "description": "Modifies payment retry scheduling to run on a recurring retry path without a bounded timeout.",
        "short_description": "Retry scheduling change with elevated reliability risk.",
        "diff": "diff --git a/services/payments/src/retry.py b/services/payments/src/retry.py\n--- a/services/payments/src/retry.py\n+++ b/services/payments/src/retry.py\n@@ -1,2 +1,3 @@\n from shared.queue import publish\n def retry_payment(payment): publish('payments.retry', payment)\n+def schedule_retry(payment): return retry_payment(payment)\n",
      },
      {
        "number": 104,
        "risk": "critical",
        "title": "Refactor payment queue and retry policy",
        "author": "alex",
        "status": "blocked",
        "files_changed": ["shared/queue.py", "services/payments/src/retry.py"],
        "date": "2026-07-20T16:45:00Z",
        "description": "Introduces an unsafe queue publish path and an unbounded retry policy that can amplify payment failures.",
        "short_description": "Critical queue and retry behavior revision with broad blast radius.",
        "diff": "diff --git a/shared/queue.py b/shared/queue.py\n--- a/shared/queue.py\n+++ b/shared/queue.py\n@@ -1 +1,2 @@\n def publish(topic, payload): return None\n+def publish_unsafe(topic, payload): return publish(topic, payload)\ndiff --git a/services/payments/src/retry.py b/services/payments/src/retry.py\n--- a/services/payments/src/retry.py\n+++ b/services/payments/src/retry.py\n@@ -1,2 +1,3 @@\n from shared.queue import publish\n def retry_payment(payment): publish('payments.retry', payment)\n+def retry_forever(payment): return retry_payment(payment)\n",
      },
    ]
