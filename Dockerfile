from ubuntu

COPY cas-req-app/dist/cas-req-app /usr/share/nginx/html

COPY app-tier/requirements.txt /tmp/requirements.txt

RUN apt update -y && \
    apt install \
    nginx \
    python3-dev \
    python3-pip \
    python \
    python-pip \
    bash \
    gcc \
    git \
    vim -y

RUN rm -rf /usr/share/nginx/html && \
    rm -rf /etc/nginx/sites-enabled/default 

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY cas-req-app/dist/cas-req-app /usr/share/nginx/html

RUN pip3 install -r /tmp/requirements.txt 

COPY uwsgi.ini /etc/uwsgi/

RUN pip install git+https://github.com/Supervisor/supervisor@master

COPY app-tier/app /app
COPY app-tier/app.conf /usr/supervisord.conf

CMD ["/usr/local/bin/supervisord","--nodaemon","-c","/usr/supervisord.conf"]