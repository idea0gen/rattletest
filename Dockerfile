FROM python:3.10

WORKDIR /app
COPY . /app


RUN pip install -r requirements/production.txt

RUN python --version
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD uwsgi --http=0.0.0.0:80 --module=config.wsgi
