FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --only-binary=:all:
COPY . .
RUN mkdir -p models
EXPOSE 5000
CMD ["python", "app.py"]
