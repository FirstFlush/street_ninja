# Use the full Python 3.10.12 base image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Install system-level dependencies for PostgreSQL + GIS
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
