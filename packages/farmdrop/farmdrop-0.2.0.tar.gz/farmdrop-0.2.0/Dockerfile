FROM ubuntu:14.04
MAINTAINER Colin Powell "colin.powell@gmail.com"
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools git
RUN easy_install pip
RUN pip install virtualenv
RUN pip install uwsgi
RUN virtualenv --no-site-packages /opt/ve/farmdrop
ADD . /opt/apps/farmdrop
ADD etc/gunicorn.conf /opt/gunicorn_farmdrop.conf
ADD etc/run.sh /usr/local/bin/run_farmdrop
RUN (cd /opt/apps/farmdrop && git remote rm origin)
RUN (cd /opt/apps/farmdrop && git remote add origin https://gitlab.com/farmdrop/farmdrop.git)
RUN (cd /opt/apps/farmdrop && python setup.py install)
EXPOSE 30321
CMD ["/bin/sh", "-e", "/usr/local/bin/run_farmdrop"]
