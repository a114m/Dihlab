FROM python:2.7-alpine3.7

ENV PYTHONUNBUFFERED 1


# Install system libs

RUN apk update
RUN apk add \
  gcc\
  python-dev\
  libxslt-dev\
  libxml2-dev\
  mysql-dev\
  libxslt-dev\
  jpeg-dev\
  zlib-dev\
  libffi-dev\
  libc-dev


RUN mkdir . /app
WORKDIR /app


# Install Python packages

ADD requirements.txt /app/
RUN pip install -r requirements.txt


# Mount and configure Django app

ADD . /app
RUN cp dihlab/settings.example.py dihlab/settings.py
RUN python manage.py collectstatic --no-input


# Expose port 8000

EXPOSE 8000


# Start app command

CMD ./run.sh
