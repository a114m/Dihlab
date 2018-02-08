#! /bin/sh

### Run app in development mode

docker-compose run --rm\
  -e ENV=development\
  -p '0.0.0.0:8000:8000'\
  web
