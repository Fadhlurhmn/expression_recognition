# Gunakan image Python
FROM python:3.9-slim

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Buat dan pindah ke direktori kerja
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Salin semua file ke dalam container
COPY . /app

# Install dependency
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port untuk FastAPI
EXPOSE 8000

# Jalankan server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
