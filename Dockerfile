# pull official base image
FROM python:3.12.4-slim-bookworm

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y dos2unix &&\
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# copy project
COPY . .

COPY start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]