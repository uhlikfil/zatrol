### BUILD UI ###
FROM node:lts-alpine AS UI_BUILD

WORKDIR /zatrol-ui
COPY zatrol-ui /zatrol-ui

RUN npm install
RUN npm run build

### BUILD BE ###
FROM python:3.9-slim-buster as BE_BUILD

WORKDIR /build
COPY setup.py ./setup.py
COPY zatrol ./zatrol
COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN python ./setup.py bdist_wheel --dist-dir /dist

### RUN ###
FROM python:3.9-slim-buster

ENV DATABASE_URL=
ENV RIOT_API_KEY=
ENV CHAMPIONS_INTERVAL_H=
ENV MATCH_HISTORY_INTERVAL_H=
ENV ASSETS_DIR=
ENV SERVER_PORT=
ENV SERVE_UI=

WORKDIR /app

# copy build artifacts
COPY assets /assets
COPY --from=UI_BUILD /zatrol-ui/build /zatrol-ui/build
COPY --from=BE_BUILD /dist ./app_wheels

# install the app
RUN pip install --upgrade pip setuptools
RUN pip install ./app_wheels/*
RUN pip install gunicorn

# run the app
ENTRYPOINT gunicorn "zatrol:wsgi()" -b 0.0.0.0:$SERVER_PORT
