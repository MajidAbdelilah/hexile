FROM python:3.9-slim

# Install system dependencies including PostgreSQL client
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    postgresql-client \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV DOCKER_API_VERSION=1.41

# Ensure PostgreSQL binaries are in PATH
ENV PATH="/usr/lib/postgresql/13/bin:${PATH}"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]