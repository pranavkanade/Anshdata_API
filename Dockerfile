FROM python:3.7-stretch

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install netcat && apt-get clean

RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

COPY ./startup.sh /usr/src/app/startup.sh

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/startup.sh"]
