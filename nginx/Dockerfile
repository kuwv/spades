FROM centos/python-38-centos7 AS docs

COPY requirements.txt mkdocs.yml ./
RUN pip install --no-cache-dir --requirement=requirements.txt

COPY ./docs ./docs
RUN mkdocs build

FROM centos/nginx-116-centos7

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf.d /etc/nginx/conf.d/
COPY --from=docs /opt/app-root/src/site/ /usr/share/nginx/html/docs/

USER root

RUN yum update-minimal --security -y ;\
    yum clean all && \
    rm -rf /var/cache/yum

USER default

EXPOSE 80 443
