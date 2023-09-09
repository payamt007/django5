version: "3.9"

services:
  redis:
    image: redis:7.2
    ports:
      - 6379:6379
  db:
    image: postgres:15.4
    env_file:
      - ./backend/.env
    ports:
      - 5432:5432
  api:
    build: ./backend
    ports:
      - 8000:8000
    env_file:
      - ./backend/.env
    volumes:
      - .:/usr/src/app
    depends_on:
      - redis
      - db
  worker:
    build: ./backend
    #command: celery -A backend.celery worker --loglevel=info --pool=solo
    command: celery -A backend.celery worker --loglevel=info -P eventlet
    env_file:
      - ./backend/.env
    depends_on:
      - redis
  beat:
    build: ./backend
    command: celery -A backend.celery beat --loglevel=info
    volumes:
      - .:/usr/src/app
    depends_on:
      - redis
  mkdocs:
    build: ./backend
    command: /bin/sh -c "python -m mkdocs build && python -m mkdocs serve -a 0.0.0.0:7000"
    volumes:
      - .:/usr/src/app
    ports:
      - 7000:7000
    depends_on:
      - api
  frontend:
    build: ./frontend
    ports:
      - 3000:3000