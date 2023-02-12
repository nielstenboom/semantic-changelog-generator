FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY main.py /main.py

ENTRYPOINT ["python", "/main.py"]