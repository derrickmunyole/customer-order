# Build stage
FROM python:3.13-alpine AS builder
ENV PYTHONUNBUFFERED 1

# Copy requirements first to leverage cache
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Create python virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Install build dependencies
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r /tmp/requirements.txt

# Final stage
FROM python:3.13-alpine
ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:/py/bin:$PATH"

# Copy built wheels from builder
COPY --from=builder /tmp/wheels /tmp/wheels
COPY --from=builder /py /py

# Install production dependencies
RUN apk add --update --no-cache \
        postgresql-client \
        nodejs \
        npm && \
    /py/bin/pip install --no-cache-dir /tmp/wheels/* && \
    rm -rf /tmp && \
    adduser --disabled-password django-user

# Copy application code
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app

# Set up permissions
RUN mkdir -p /app/cov && \
    chmod -R +x /scripts && \
    chown -R django-user:django-user /app

EXPOSE 8000

CMD ["run.sh"]
