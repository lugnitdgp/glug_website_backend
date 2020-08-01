![Django CI](https://github.com/lugnitdgp/glug_website_backend/workflows/Django%20CI/badge.svg?branch=master)
![Backend CD](https://github.com/lugnitdgp/glug_website_backend/workflows/Backend%20CD/badge.svg?branch=prod)
# GLUG Website Public Repo
We are using django REST framework for backend api. <br />
And Vue.js for frontend. <br />

#### Click [here](https://documenter.getpostman.com/view/5813355/RzZ7mzS4) to refer to the api documentation.

---
Use a virtual envionment for installing this, 
i.e `venv` or `pipenv`.
### Install Dependencies
For debian based distro, *in virtual evironment* terminal type
```shell
pip install -r requirements.txt
```
### To run the project on local machine
Create a PostgresSQL database.</br>
Then `cp .env.example .env` and change `.env` file according to your need.

Inside project directory type
```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

# To run with development settings
python3 manage.py runserver --settings=glug_website.dev-settings
```

## Development Environment Config
This project uses PEP8 code style, please make sure to follow. Yapf is our preffered formatting tool.
If you are using VSCode add the following in your *settings.json* 
```
"python.formatting.provider": "yapf",
"python.formatting.yapfArgs": ["--style={based_on_style: pep8, indent_width: 4, column_limit: 120}"],
"python.linting.enabled": true
