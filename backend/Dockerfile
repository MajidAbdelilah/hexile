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

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Expose port and run the Django development server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]