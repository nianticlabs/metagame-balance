# Base Image
FROM ubuntu:18.04

# run updates, upgrades, common
RUN apt update \
    && apt upgrade \
    && apt install software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update

# ssh remote access
EXPOSE 22
RUN apt-get -y install sudo openssh-server \
	&& adduser --shell /bin/bash --ingroup sudo --gecos '' --disabled-password guest \
	&& echo 'guest:123' | chpasswd \
	&& echo "X11UseLocalhost no" >> /etc/ssh/sshd_config

# python3 install
RUN apt install python3.8

# git install
RUN apt install git

# pokemon vgc engine repository clone
RUN git clone https://gitlab.com/DracoStriker/pokemon-vgc-engine.git

# install requirements


# Run SSH
CMD service ssh start -D
