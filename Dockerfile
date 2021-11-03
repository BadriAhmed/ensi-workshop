FROM python:3.8.9-slim
WORKDIR /app
RUN apt-get update && apt-get install sox -y && apt-get install libsndfile1 -y && apt install ffmpeg -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
