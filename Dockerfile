# Use Python 3.13 Alpine as the base image for a lightweight container
FROM python:3.13-alpine
LABEL maintainer: "Derrick"

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

WORKDIR /app
# Expose port 8000 for the Django development server
EXPOSE 8000

ARG DEV=false

# Execute multiple commands in a single RUN to reduce image layers:
RUN python -m venv /py && \
    # Upgrade pip to latest version
    /py/bin/pip install --upgrade pip && \
    # Install PostgreSQL client for database operations
    apk add --update --no-cache postgresql-client && \
    # Install temporary build dependencies needed for Python packages
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    # Install Python dependencies from requirements files
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ ${DEV}="True" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Clean up temporary files
    rm -rf /tmp && \
    # Remove temporary build dependencies to reduce image size
    apk del .tmp-build-deps && \
    # Create a non-root user for security
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # Make scripts executable
    chmod -R +x /scripts

# Add scripts and virtual environment to PATH
ENV PATH="/scripts:/py/bin:$PATH"

# Switch to non-root user for security
USER django-user

# Execute run.sh script when container starts
CMD ["run.sh"]
