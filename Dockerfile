FROM python:3.7-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY pipe /

ENTRYPOINT ["python3", "/pipe.py"]