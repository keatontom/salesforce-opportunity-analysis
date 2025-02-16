# Use a lightweight Python image
FROM python:3.12-slim AS backend
WORKDIR /app  # ✅ Set root directory inside Docker container

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# ✅ Copy the backend folder into the container
COPY backend /app/backend

# ✅ Change working directory to backend
WORKDIR /app/backend

# Set permissions for security
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the FastAPI backend port
EXPOSE 8000

# ✅ Correct CMD to start FastAPI (No `backend.` prefix)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]