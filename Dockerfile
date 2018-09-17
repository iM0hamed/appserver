FROM kennethreitz/pipenv

ADD . /app
WORKDIR /app

EXPOSE 8000

RUN pipenv install