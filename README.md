# Heroku Django Starter Template

An utterly fantastic project starter template for Django 3.0.

## Features

* Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
* Enhancements to Django's static file serving functionality via WhiteNoise.
* Latest Python 3.8.3 runtime environment.

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install Django ( `$ pipenv install django` )
3. Create a new project using this template

## Creating Your Project

Create a new Django app is easy::

    $ django-admin.py startproject --name=Procfile helloworld

(If this doesn't work on windows, replace `django-admin.py` with `django-admin` )

You can replace ` ` helloworld ` ` with your desired project name.

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.

## License: MIT

## Further Reading

* [Gunicorn](https://warehouse.python.org/project/gunicorn/)
* [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
* [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
