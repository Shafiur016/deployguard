# Failure injection and recovery runbook

**Warning:** Only run in your local demo environment, never on production traffic.

1. `cp .env.example .env`; set `GRAFANA_PASSWORD` to a unique value.
2. Start: `docker compose up --build -d`. Confirm `curl -f localhost:8002/healthz` and `/readyz` return 200.
3. Open Prometheus at `http://localhost:9090`, Grafana at `http://localhost:3000`, Alertmanager at `http://localhost:9093`.
4. Simulate a readiness failure: change `DG_FAIL_READINESS=1` in `.env` and run `docker compose up -d --force-recreate api`. `/readyz` now returns HTTP 503 while `/healthz` remains 200.
5. Observe `deployguard_ready == 0`; after one minute Prometheus should fire `DeployGuardNotReady`. Prometheus alert rules are viewable in Alerts UI; alertmanager uses a **no-op demo receiver**.
6. Recover: set `DG_FAIL_READINESS=0` in `.env`, `docker compose up -d --force-recreate api`, verify `/readyz` is 200 and `deployguard_ready == 1`.
7. Run `python scripts/smoke_requests.py --count 100` to produce request/latency metrics.
8. Rollback example: `docker compose pull` after tagging a prior known-good image, or rebuild the previous Git commit. **The CI/CD pipeline does not automatically roll back**.

This exercise demonstrates readiness health, alert generation, and manual recovery. It does not constitute a tested production failover or disaster recovery system.
