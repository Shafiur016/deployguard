FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home appuser
COPY service ./service
USER appuser
EXPOSE 8002
HEALTHCHECK --interval=20s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8002/readyz', timeout=3)" || exit 1
CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "8002"]
