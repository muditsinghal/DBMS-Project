FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /server
COPY . /server/

RUN pip3 install -r requirements.txt
