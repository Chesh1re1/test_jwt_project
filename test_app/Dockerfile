FROM python:3.11-slim

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/test_app
COPY requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    sed -i 's/\r$//' /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
