FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgomp1 \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/server.py"]
