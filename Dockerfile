FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .
RUN python manage.py collectstatic --noinput \
    && mkdir -p /app/media \
    && chown -R 10001:10001 /app /opt/venv

USER 10001:10001
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_pcm && python -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'AdminPCM2026!')\" && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
