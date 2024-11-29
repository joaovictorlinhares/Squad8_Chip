FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir opencv-python-headless

COPY geracao_frames/app/ ./

RUN mkdir -p /app/volumeFrame

CMD ["python", "geracao_frames.py"]