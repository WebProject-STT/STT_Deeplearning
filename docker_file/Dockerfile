FROM ubuntu:18.04
ENV TZ=US/Central
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PORT = 8090

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && \ 
    apt-get install -y --no-install-recommends apt-utils && \ 
    apt-get -y install software-properties-common && \ 
    add-apt-repository -y ppa:deadsnakes/ppa && \ 
    apt-get update --fix-missing && \ 
    apt-get -y install --fix-missing python3.7 && \ 
    apt-get -y install --fix-missing python3.7-dev && \ 
    apt-get -y install --fix-missing python3-pip && \ 
    python3.7 -m pip install pip --upgrade

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# mecab start
RUN apt-get update && \ 
    apt-get install -y --no-install-recommends tzdata g++ git curl
RUN apt-get install python3-setuptools
RUN apt-get install -y default-jdk default-jre

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
RUN update-alternatives --config python3 
RUN cd ${APP_HOME} && \ 
    curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -s

ENV FLASK_APP=main.py

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

EXPOSE 8090

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 30 main:app
