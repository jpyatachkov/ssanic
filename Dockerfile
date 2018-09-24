FROM python:3.6

RUN apt-get update

RUN mkdir -p /var/www/ssanic
ADD . /var/www/ssanic
ADD ./httpd.conf /etc/httpd.conf

WORKDIR /var/www/ssanic

RUN pip install -r requirements.txt && python setup.py install

WORKDIR /

EXPOSE 80

CMD ssanic --config-file /etc/httpd.conf
