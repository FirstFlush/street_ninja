# 1. Use the full Python 3.10.12 base image
FROM python:3.10.12-bullseye

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system-level dependencies for PostgreSQL + GIS
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy only the requirements file first (leverages Docker caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire project into the container
COPY . .

# 7. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=street_ninja_server.settings \
    CELERY_BROKER_URL=redis://redis:6379/0 \
    CELERY_RESULT_BACKEND=redis://redis:6379/0

# 8. Expose port for Gunicorn
EXPOSE 8000

# 9. Set entrypoint to start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "street_ninja_server.wsgi:application"]
