FROM python:3.11-slim
WORKDIR /app

# Install build deps if needed
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use PORT env provided by Back4App at runtime
EXPOSE  ${PORT:-5000}

# Use sh -c so ${PORT} expands at container start
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT:-5000} app:app"]