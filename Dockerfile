FROM ubuntu:latest

RUN useradd -m -p web -s /bin/bash web
RUN echo "web:web" | chpasswd

RUN apt update
RUN apt -y upgrade
RUN apt install -y python3-pip sqlite3

COPY . /app
WORKDIR /app

RUN chown -R web /app
RUN chown -R web /home/web

USER web

RUN pip3 install -r deploy/requirements.txt

ENV PATH $PATH:/home/web/.local/bin

RUN flask db upgrade

EXPOSE 5000
CMD ["python3", "src/app.py"]