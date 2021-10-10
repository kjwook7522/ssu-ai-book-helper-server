FROM python:3.8

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . book_server/

WORKDIR /book_server

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "book_server.wsgi:application" ]