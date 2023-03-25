FROM python:3.10-slim

LABEL org.opencontainers.image.source=https://github.com/LP0101/jellyfin-exporter-py

RUN mkdir /app
WORKDIR /app
COPY * /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "exporter.py"]