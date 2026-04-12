FROM python:3.9-slim
WORKDIR /app
COPY . .
# Agora ele instala tudo que estiver na lista do requirements
RUN pip install -r requirements.txt 
CMD ["python", "app.py"]