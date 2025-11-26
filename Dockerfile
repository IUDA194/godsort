FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/app

WORKDIR /app
COPY . .

CMD ["python godsort.py"]



