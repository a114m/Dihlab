FROM python:2.7-alpine3.7
ADD . /app
WORKDIR /app


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


# Install python packages
RUN mv dihlab/settings.example.py dihlab/settings.py
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input


EXPOSE 8000

CMD ./run.sh
