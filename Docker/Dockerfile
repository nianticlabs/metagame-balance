# base image
FROM ubuntu:18.04

# updates, upgrades, common instalation
RUN apt-get update \
    && apt-get upgrade \
    && apt-get install software-properties-common

# python3 install
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install python3.8 \
    && apt-get install python3.8-venv \
    && apt-get install python3.8-dev

# pip upgrade
RUN python3 -m pip install --user --upgrade pip

# install and create virtualenv
RUN python3 -m pip install --user virtualenv \
    && python3 -m venv vgc-env

# git install
RUN apt-get install git-all

# vgc ai framework repository clone
RUN git clone https://gitlab.com/DracoStriker/pokemon-vgc-engine.git vgc-ai

# install requirements
RUN source vgc-env/bin/activate \
    && python3 -m pip install -r vgc-ai/requirements.txt \
    && deactivate

# ssh remote access
EXPOSE 22
RUN apt-get -y install sudo openssh-server \
	&& adduser --shell /bin/bash --ingroup sudo --gecos '' --disabled-password trainer \
	&& echo 'trainer:pkm' | chpasswd \
	&& echo "X11UseLocalhost no" >> /etc/ssh/sshd_config

# Run SSH
CMD service ssh start -D
