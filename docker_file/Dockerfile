FROM ubuntu:18.04
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PORT = 5000

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN cp /etc/apt/sources.list /etc/apt/sources.list.org
RUN sed -e 's/\(us.\)\?archive.ubuntu.com/ftp.daumkakao.com/g' -e 's/security.ubuntu.com/ftp.daumkakao.com/g' < /etc/apt/sources.list.o


# mecab start
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl
RUN apt-get install -y wget build-essential autotools-dev automake libmecab2 libmecab-dev git
RUN apt-get install -y default-jdk default-jre
RUN apt-get install -y python3 python3-pip python3-dev

RUN wget -O - https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz | tar zxfv -
RUN cd mecab-0.996-ko-0.9.2; ./configure; make; make install; ldconfig

RUN wget -O - https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz | tar zxfv -
RUN cd mecab-ko-dic-2.1.1-20180720; sh ./autogen.sh
RUN cd mecab-ko-dic-2.1.1-20180720; ./configure; make; make install; ldconfig

RUN git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
RUN cd mecab-python-0.996; python3 setup.py build; python3 setup.py install

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get remove -y build-essential
RUN rm -rf mecab-*

ENV FLASK_APP=main.py

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

VOLUME ["/data"]
EXPOSE 5000

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 main:app
