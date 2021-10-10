FROM python:3.8

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . ai_server/

WORKDIR /ai_server

CMD [ "python3", "server.py" ]