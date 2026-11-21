# DeployGuard — CI/CD and Service Observability Demo

GitHub Actions tests and builds a containerized FastAPI service and publishes immutable GHCR release tags. Docker Compose provisions Prometheus, Alertmanager and Grafana. Terraform manages a **local Docker container** for infrastructure-as-code practice (no cloud bill).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn service.app:app --host 127.0.0.1 --port 8002
# curl http://localhost:8002/metrics
```

## Full observability stack

```bash
cp .env.example .env
# Change the Grafana password in .env
docker compose up --build -d
```

- API: http://localhost:8002/docs
- Metrics: http://localhost:8002/metrics
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Grafana: http://localhost:3000 (Grafana provisioned dashboard)
- See `docs/RECOVERY_RUNBOOK.md` for a reproducible readiness failure and recovery exercise.

## Terraform (optional, separate instance)

```bash
cd terraform
terraform init && terraform plan && terraform apply
curl http://localhost:8003/healthz
terraform destroy
```

Terraform uses your **local Docker daemon**; it does not deploy AWS infrastructure. Docker Compose and Terraform create separate instances, intentionally using ports 8002 and 8003.

## CI/CD and security limitations

`.github/workflows/ci.yml` runs compile/test, builds the container and pushes GHCR images **only for `v*` tags**. Publishing does not deploy to a server or perform automatic rollback; set up a deployment target and approval gate before claiming continuous deployment. Local monitoring demo has exposed ports; bind them to localhost or protect with network policies for non-local use. Alertmanager's receiver is a no-op demo, not actual notifications. For a production system add image signing, pinned-action SHAs, vulnerability scans and infrastructure-specific deployment credentials.
