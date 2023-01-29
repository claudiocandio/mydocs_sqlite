# syntax=docker/dockerfile:1
FROM python:3.10.6
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -ex; \
    apt-get update; \
    apt-get install -y sqlite3; \
    apt-get install -y python3-dev default-libmysqlclient-dev default-mysql-client build-essential; \
    apt-get install -y --no-install-recommends \
        vim;
WORKDIR /mydocs_sqlite
COPY requirements-mydocs.txt /mydocs_sqlite/
COPY mydocs_sqlite/ /mydocs_sqlite/
RUN pip install -r requirements-mydocs.txt
#CMD python manage.py runserver 0.0.0.0:8000
