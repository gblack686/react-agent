FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Install Node.js and npm for MCP servers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install MCP tooling
RUN npm install -g @smithery/cli

# Copy the rest of the application
COPY . .

# Setup environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose ports for LangGraph and MCP servers
EXPOSE 8000
EXPOSE 8080

# Start the LangGraph application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"] 