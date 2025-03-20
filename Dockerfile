
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive


RUN apt update && apt install -y \
    wget \
    curl \
    sudo \
    net-tools \
    vim \
    nano\
    ufw \
    && rm -rf /var/lib/apt/lists/* 


WORKDIR /root


CMD ["/bin/bash"]
