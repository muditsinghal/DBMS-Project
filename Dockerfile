FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /server
COPY ./requirements.txt /server/
RUN pip3 install -r requirements.txt
COPY . /server/
RUN chmod +x wait-for-it.sh
RUN chmod +x docker-entry.sh
