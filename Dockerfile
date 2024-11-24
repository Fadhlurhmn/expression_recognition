# Gunakan base image Python yang mendukung TensorFlow
FROM python:3.9-slim

# Install dependency sistem untuk OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Buat direktori aplikasi
WORKDIR /app

# Salin requirements.txt dan install dependensi Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode aplikasi
COPY . .

# Jalankan aplikasi FastAPI dengan Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
