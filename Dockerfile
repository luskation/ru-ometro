# Stage 1: install dependencies into an isolated virtualenv
FROM python:3.12-slim AS deps
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime image with only the venv and the app code
FROM python:3.12-slim AS runtime
ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 1000 appuser
WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
COPY app/ ./app/

USER 1000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
