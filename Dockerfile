FROM python:3.8

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD book_server book_server

WORKDIR /book_server

CMD [ "python", "manage.py", "runserver", "0.0.0.0:5000", "--insecure" ]