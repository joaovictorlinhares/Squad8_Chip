FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    opencv-python-headless \
    requests \
    ultralytics \
    watchdog

COPY deteccao_frames/app/ ./

RUN mkdir -p /app/volumeFrame

CMD ["python", "deteccao_frames.py"]