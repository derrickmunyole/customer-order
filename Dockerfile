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
    # Install Cython for building wheels
    /py/bin/pip install cython && \
    # Create wheels directories and build all wheels
    mkdir -p /tmp/wheels/prod /tmp/wheels/dev && \
    /py/bin/pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels/prod -r /tmp/requirements.txt && \
    /py/bin/pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels/dev -r /tmp/requirements.dev.txt

# Final stage
FROM python:3.13-alpine
ARG DEV=false
ENV PYTHONUNBUFFERED 1

# Copy wheels and virtual environment
COPY --from=builder /tmp/wheels/prod /tmp/wheels/prod
COPY --from=builder /tmp/wheels/dev /tmp/wheels/dev
COPY --from=builder /py /py

# Copy application code
COPY ./app /app
WORKDIR /app

# RUN command for container setup
RUN apk add --update --no-cache \
        postgresql-client \
        nodejs \
        npm && \
    /py/bin/pip install --no-cache-dir /tmp/wheels/prod/* && \
    if [ "$DEV" = "true" ] ; then \
        /py/bin/pip install --no-cache-dir /tmp/wheels/dev/* ; \
    fi && \
    rm -rf /tmp && \
    adduser --disabled-password django-user && \
    mkdir -p /app/cov && \
    chown -R django-user:django-user /app

ENV PATH="/py/bin:$PATH"

EXPOSE 8000

CMD ["run.sh"]
