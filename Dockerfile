FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /server
COPY . /server/

RUN pip3 install -r requirements.txt

# RUN python3 Carpooling/manage.py makemigrations
# RUN python3 Carpooling/manage.py migrate
# RUN python3 Carpooling/manage.py runserver 