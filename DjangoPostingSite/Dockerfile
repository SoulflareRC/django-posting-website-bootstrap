FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE DjangoPostingSite.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip 
COPY ./requirements.txt /app/ 
RUN pip install -r requirements.txt 

COPY . /app/ 

# RUN python manage.py makemigrations posts
# RUN python manage.py migrate
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic

# CMD ["python","manage.py","runserver","0.0.0.0:8000"]
# CMD ["gunicorn","DjangoPostingSite.wsgi:application","--bind","0.0.0.0:8000"]

EXPOSE 8000 