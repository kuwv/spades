FROM centos/python-38-centos7 AS docs

COPY requirements.txt mkdocs.yml ./
RUN pip install --no-cache-dir --requirement=requirements.txt

COPY ./docs ./docs
RUN mkdocs build

FROM centos:7

WORKDIR /usr/share/nginx

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=docs /opt/app-root/src/site/ /usr/share/nginx/html/docs/

USER root

RUN yum update-minimal --security -y ;\
    yum install epel-release -y

RUN yum install nginx -y ;\
    chown -R nginx:nginx /etc/nginx/conf.d/ssl ;\
    yum clean all && \
    rm -rf /var/cache/yum

# USER nginx

EXPOSE 80 443

CMD nginx -g 'daemon off;'
