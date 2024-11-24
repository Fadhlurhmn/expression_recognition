# Gunakan base image Python yang ringan
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Install semua dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Expose port untuk aplikasi
EXPOSE 8000

# Tambahkan perintah chmod di Dockerfile
RUN chmod +x start.sh

# Command untuk menjalankan aplikasi
CMD ["sh", "start.sh"]
