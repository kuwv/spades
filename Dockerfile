FROM centos/python-38-centos7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production

COPY ./ ./

USER root

RUN yum update-minimal --security -y ;\
    yum clean all && \
    rm -rf /var/cache/yum

USER default

RUN pip install --no-cache-dir --requirement=requirements.txt

CMD [ "gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--worker-class", "gevent", "--workers", "1" ]
