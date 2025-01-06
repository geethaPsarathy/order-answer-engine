# 1) Base image: choose Python 3.10 (or your preferred version)
FROM python:3.10-slim

# 2) Set a working directory
WORKDIR /app

# 3) Copy requirements first for caching
COPY requirements.txt /app/

# 4) Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy your FastAPI code
COPY . /app/

# 6) Expose FastAPI port
EXPOSE 8000

# 7) Start your app (adjust "main:app" to your actual entry point)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
