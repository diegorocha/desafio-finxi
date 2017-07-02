FROM python:3.4-alpine
MAINTAINER Diego Rocha

ADD . /var/www
WORKDIR /var/www

# Garante um SQlite vazio
RUN rm /var/www/aluguel/db.sqlite3

# Dependências do Pillow
RUN apk add --no-cache gcc zlib zlib-dev jpeg-dev musl-dev
RUN ln -s /lib/libz.so /usr/lib/

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python manage.py test

ENV DEBUG=False
EXPOSE 8000
CMD ["gunicorn", "aluguel.wsgi", "-b", "0.0.0.0:8000", "-d"]