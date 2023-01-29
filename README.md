[![Language Python](https://img.shields.io/badge/language-python-blue)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-4.0-success)](https://www.djangoproject.com/)
[![docker](https://img.shields.io/badge/docker-compose-success)](https://www.docker.com/)
[![GitHub license](https://claudiocandio.github.io/img/license_mit.svg)](https://github.com/claudiocandio/gemini-api/blob/master/LICENSE)

# MyDocs - django docker web application

MyDocs is a simple but functional web application useful to catalog documents, it is developed using the Django framework and Python. I'm using it to store all my personal data in a SQLite database (yes I know some do not recommend saving files to a database, but I have my reasons;-)  
Any kind of file can be saved up to a size of 300MB configurable, documents, invoices, medical reports, pay slips, photos, software, anything.

A document saved to MyDocs may include files attachments, it can have one or more Owners, one or more Categories, a Date field and Notes. It is possible to configure multiple users with different databases assigned. MyDocs also works well with mobile phones.

## MyDocs Install

```bash
$ wget https://github.com/claudiocandio/mydocs_sqlite/raw/main/docker-compose.yml
$ docker-compose up -d
```

**Make Database persistent and add Settings file**  

```bash
$ docker cp mydocs:/mydocs_sqlite/db.sqlite3 .
$ docker cp mydocs:/mydocs_sqlite/mydocs/settings.py .
```

Edit docker-compose.yml and uncomment the volumes entries:  
&emsp;volumes:  
&emsp;&emsp;- ./settings.py:/mydocs_sqlite/mydocs/settings.py  
&emsp;&emsp;- ./db.sqlite3:/mydocs_sqlite/db.sqlite3  

Restart mydocs

```bash
$ docker-compose restart
```

**Upgrade MyDocs**  
```bash
$ docker-compose down
$ docker-compose pull
$ docker-compose up -d
```

**Access MyDocs**  
http://server-ip:8000  
Login: admin  
Password: admin

**Access Django Admin**  
http://server-ip:8000/admin  
Login: admin  
Password: admin

Users with Django Superuser permission, like admin, can access the Django Admin site, add new users, manage databases from MyDocs Settings and assign users to databases.

**Stop MyDocs**
```bash
$ docker-compose stop
```

## Some screnshoots

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs1.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs2.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs3.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs4.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs5.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs6.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs7.jpg)  

![mydocs](https://raw.githubusercontent.com/claudiocandio/claudiocandio.github.io/main/img/mydocs/mydocs8.jpg)  

## Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
