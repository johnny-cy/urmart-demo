FROM ubuntu:20.04
RUN mkdir /workspace
RUN apt update \
    && apt install -y python3.8 \
    && apt install -y python3-pip \
    && pip3 install django==3.1 \
    && pip3 install channels==3.0.3 \
    && pip3 install channels_redis==3.2.0 \
    && pip3 install pandas==1.2.2 \
    && pip3 install uwsgi==2.0.19.1 \
    && pip3 install requests==2.25.1 \
    && apt install -y vim \
    && apt install -y iputils-ping \
    && apt install -y lsof \
    && apt install -y telnet \
    && apt install -y curl 
CMD ["/app/run.sh"]
