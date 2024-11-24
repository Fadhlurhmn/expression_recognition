# Gunakan image Python slim
FROM python:3.9-slim

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Buat dan pindah ke direktori kerja
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Salin semua file proyek ke container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port untuk FastAPI
EXPOSE 8000

# Jalankan server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
