FROM python:3.10

COPY main.py /main.py

ENTRYPOINT ["python", "/main.py"]