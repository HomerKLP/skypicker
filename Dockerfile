FROM python:3.6

WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
RUN python manage.py migrate

EXPOSE 8000

CMD [ "gunicorn", "-b 0.0.0.0:8000", "--workers=4", "skypicker.wsgi" ]
