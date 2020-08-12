# To build use:
# docker build -t pram .
# docker create --name pram0 --network host  -t -i pram
# and create other containers

#$ docker start -a -i pram0

# docker inspect <container name or container id>
# Nginx


FROM ubuntu:18.04
#ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y git python3-pip python3-psutil net-tools
RUN pip3 install pip install git+https://github.com/momacs/pram.git
RUN pip3 install attrs --upgrade
RUN pip3 install cherrypy
RUN pip3 install lxml
RUN pip3 install jinja2
RUN pip3 install flask
RUN git clone https://github.com/momacs/pram
RUN cd pram/src/sim/01-simple && python3 sim.py


