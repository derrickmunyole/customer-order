# Build stage
FROM python:3.13-alpine AS builder
ARG DEV=False
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
    /py/bin/pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r /tmp/requirements.txt && \
    ARG DEV=false \
    if [ "$DEV" == "True" ] ; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
    fi


# Final stage
FROM python:3.13-alpine
ENV PYTHONUNBUFFERED 1

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

ENV PATH="/py/bin:$PATH"

# Copy application code
COPY ./app /app
WORKDIR /app

# Set up permissions
RUN mkdir -p /app/cov && \
    chown -R django-user:django-user /app

EXPOSE 8000

CMD ["run.sh"]
