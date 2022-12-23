FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY docker/requirements.txt .

# copy django scripts
COPY docker/scripts/* /usr/local/bin/

# install requirements
RUN pip install --upgrade pip \
    pip install -r requirements.txt

WORKDIR /code

COPY . .

WORKDIR /code/src

LABEL maintainer jakub-mrow
LABEL Project=django-skeleton