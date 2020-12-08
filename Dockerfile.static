FROM centos/python-38-centos7 AS docs

COPY ./requirements.txt ./
COPY ./mkdocs.yml ./
COPY ./docs/ ./

RUN pip install --user --requirement=requirements.txt
#     mkdocs build

FROM centos/nodejs-12-centos7 AS webui

COPY ./webui/package*.json ./

RUN npm install

COPY ./webui/ ./

RUN npm run build

FROM centos/nodejs-12-centos7

# COPY --from=docs /opt/app-root/src/site/ /usr/share/nginx/html/docs/
COPY --from=webui /opt/app-root/src/dist/ /usr/share/nginx/html/spades-ui/

# COPY nginx.conf /etc/nginx/nginx.conf
# COPY conf.d /etc/nginx/conf.d/
# COPY --from=build /usr/local/src/dist /usr/share/nginx/html

EXPOSE 80 443
