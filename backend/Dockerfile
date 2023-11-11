FROM python:3.9.6

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Layer for system requirements.
RUN apt-get update \
     && apt-get -y install gcc libpq-dev python3-dev netcat git \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --default-timeout=2000 -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
