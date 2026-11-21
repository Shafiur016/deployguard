"""Instrumented sample backend that DeployGuard builds, releases, and monitors."""
import os
import time
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title='DeployGuard Reference API', version='1.0.0')
REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'route', 'status'])
LATENCY = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'route'])
READY = Gauge('deployguard_ready', 'Whether API is ready to serve traffic')

def is_ready():
    return os.getenv('DG_FAIL_READINESS', '0') not in {'1', 'true', 'yes'}

@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        route = getattr(request.scope.get('route'), 'path', 'unmatched')
        REQUESTS.labels(request.method, route, '500').inc()
        LATENCY.labels(request.method, route).observe(time.perf_counter() - started)
        raise
    route = getattr(request.scope.get('route'), 'path', 'unmatched')
    if request.url.path != '/metrics':
        REQUESTS.labels(request.method, route, str(response.status_code)).inc()
        LATENCY.labels(request.method, route).observe(time.perf_counter() - started)
    return response

@app.get('/healthz')
def health():
    return {'status': 'alive', 'service': 'deployguard'}

@app.get('/readyz')
def readiness(response: Response):
    ready = is_ready()
    READY.set(1 if ready else 0)
    if not ready:
        response.status_code = 503
    return {'ready': ready}

@app.get('/metrics')
def metrics():
    READY.set(1 if is_ready() else 0)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get('/api/ping')
def ping():
    return {'message': 'pong'}
