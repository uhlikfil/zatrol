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

EXPOSE 8080

ENV DATABASE_URL=
ENV API_KEY=
ENV CHAMPS_INTERVAL_H=
ENV HISTORY_INTERVAL_H=
ENV RESOURCES=/resources
ENV UI_BUILD=/zatrol-ui/build
ENV SERVE_UI=1

WORKDIR /app

# copy build artifacts
COPY resources /resources
COPY --from=UI_BUILD /zatrol-ui/build /zatrol-ui/build
COPY --from=BE_BUILD /dist ./app_wheels

# install the app
RUN pip install --upgrade pip setuptools
RUN pip install ./app_wheels/*

# run the app
CMD uvicorn --factory "zatrol:create_app" --host 0.0.0.0 --port 8080
