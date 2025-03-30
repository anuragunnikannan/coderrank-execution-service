FROM python:3.11-slim

RUN apt-get update && apt-get install -y default-jdk && apt-get install -y g++

WORKDIR /app

COPY runner.py .

CMD ["/bin/bash"]