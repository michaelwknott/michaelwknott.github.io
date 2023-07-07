Title: Using PostgreSQL with Django
Date: 2023-02-14 15:30
Modified: 2023-02-21 13:30
Category: Notes
Tags: django, postgres, notes
Slug:
Authors: Michael Knott
Summary: Configure PostreSQL for Django
Status: published

This blog post will act as a personal reminder of configuring Postsgres for a Django project.

### Create Database

Start Postgres:

`sudo service postgresql start`

Log-in to a Postgres interactive session:

`sudo -u postgres psql`

Create a database for the Django project. My project is called ar10_tracker so I'll name my database the same:

`CREATE DATABASE ar10_tracker;`

Create a user and password to interact with the database:

`CREATE USER myuser WITH PASSWORD 'mypassword';`

We can change configuration settings to optimise the performance of the database. See [documentation](https://docs.djangoproject.com/en/4.1/ref/databases/#optimizing-postgresql-s-configuration) for more information.

`ALTER ROLE myuser SET client_encoding TO 'utf8';`

`ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE myuser SET timezone TO 'UTC';`

Next we give the ar10user the required privileges to have full control over the database:

`GRANT ALL PRIVILEGES ON DATABASE ar10_tracker TO myuser;`

The postgres database is now setup and we can exit the interactive session:

`\q`


### Add required dependencies

To connect to Postgres I'll need a database adapter. I'm using [psycopg2](https://pypi.org/project/psycopg2/). Additionally to configure the database settings I require [dj_database_url](https://pypi.org/project/dj-database-url/) and [python-decouple](https://pypi.org/project/python-decouple/).

```
echo psycopg2~=2.9.5 >> requirements.in
echo dj-database-url 1.2.0 >> requirements.in
echo python-decouple==3.7 >> requirements.in
pip-compile requirements.in
python -m pip install requirements.txt
```

dj_database_url is a utility which uses a DATABASE_URL environment variable to create a dictionary containing the data specified in the DATABASE_URL string.

For example, passing the url schema for a Postgres database `postgres://myuser:mypassword@127:0.0.1:5432/ar10_tracker` to `dj_database_url.config()` will return the following dictionary:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ar10_tracker',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

python-decouple provides the functionality to separate project settings from code. I can store sensitive data such as database credentials in a separate .env file and load them as environment variables at runtime. In this Django project I'm using python-decouple to load secret key, debug status, allowed hosts and database connection credentials.

### Generating a secret key for Postgres database

`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### Utilise a .env file to store sensitive environment variables

The .env file contains the following variables:

```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DATABASE_URL=
```

### Configure Django project settings.py file to use Postgres database

Add the following imports to settings.py:

```
import dj_database_url
from decouple import Csv, config
```

Update the DATABASES variable in settings.py to utlise dj_database_url:

`DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}`


The following default variables are removed:

```
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z_)j=_h=5fmfob9l#vm)p)(#w7-w-v!p57eh^=36-jfmcoaf7t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
```

and updated to utilise the python-decouple `config` function to load environment variables from the .env file:

```
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
```



I used the following article as a guide:
<https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04>
