# Gunakan image Python
FROM python:3.11

# Set working directory
WORKDIR /app

# Salin requirements.txt dan instal dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode ke dalam container
COPY . /app/

# Expose port yang digunakan Django (Gunicorn) dan gRPC
EXPOSE 8001 50051
