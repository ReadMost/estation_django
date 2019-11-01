FROM python:3

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgdal-dev \
        nano

COPY requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8085

#RUN adduser --disabled-password --gecos '' myuser
CMD ["python3", "manage.py", "runserver", "[::]:8085"]