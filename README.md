![Django CI](https://github.com/himanshu272/glug_website_backend/workflows/Django%20CI/badge.svg?branch=master)
# GLUG Website Public Repo
We are using django REST framework for backend api. <br />
And Vue.js for frontend. <br />

#### Click [here](https://documenter.getpostman.com/view/5813355/RzZ7mzS4) to refer to the api documentation.

---
Use a virtual envionment for installing this, 
i.e `venv` or `pipenv`.
### Install Dependencies

    - python 3.6.x
    - django 2.0.x
    - pillow 5.1.x
    - djangorestframework 3.8.x
    - django-ckeditor 5.5.x
    - psycopg2 2.7.x
    - python-decouple 3.1
    - django-cors-headers 2.2.x

For debian based distro, in virtual evironment terminal type
```shell
pip install -r requirements.txt
```
### To run the project on local machine
Create a PostgresSQL database.</br>
Then `cp .env.example .env` and change `.env` file according to your need.

Inside project directory type
```shell
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py runserver
```

