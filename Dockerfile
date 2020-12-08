FROM centos/python-38-centos7

# RUN useradd -md /app webapp

WORKDIR /app
COPY . /app

RUN pip install --user --requirement=requirements.txt
# RUN yum update -y ;\
#   yum install -y \
#     gcc \
#     python38-devel \
#     python38-setuptools ;\
#   pip install --no-cache-dir -r requirements.txt ;\
#   yum remove gcc -y ;\
#   yum clean all && \
#   rm -rf /var/cache/yum

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "-p", "8000", "app:app"]
