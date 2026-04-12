FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Esta é a linha que faz o "motor" ligar:
CMD ["python", "app.py"]
