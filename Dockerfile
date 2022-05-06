FROM centos:latest

RUN yum install python3 -y & yum install git -y

RUN pip3 install --upgrade pip

RUN pip3 install flask

EXPOSE 8080

RUN git clone https://github.com/HardikTilwani/DevOps-Assistant-FE.git

RUN cd DevOps-Assitant-FE

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
