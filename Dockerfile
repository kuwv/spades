# FROM node:lts-alpine AS build
FROM centos/nodejs-12-centos7 AS build

WORKDIR /app

COPY ./static/package*.json /app/

RUN yum install -y python3 ;\
  npm install @vue/cli @vue/cli-service-global -g ;\
  npm install

COPY ./static /app

RUN npm run build

# FROM python:3.7-alpine
FROM centos/python-38-centos7

# RUN useradd -md /app webapp

WORKDIR /app
COPY . /app
RUN rm -rf /app/static
COPY --from=build /app/dist /app/static/dist

RUN yum update -y ;\
  yum install -y \
    gcc \
    python38-devel \
    python38-setuptools ;\
  pip install --no-cache-dir -r requirements.txt

# USER webapp
CMD ["daphne", "-b", "0.0.0.0", "-p", "3000", "app:app"]
