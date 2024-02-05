# SECURED API RESTFUL USING DJANGO REST FRAMEWORK
***
## Project description
***
This project is the creation of an API for an application. 
We have users than can create projects and add contributors to them.
Only contributors can access the project and create comments and issues.
Only author can modify, update and delete one of his post.
The API is secured with authentications and permissions.
***
## Installation
***
First create a folder to put the project in.
To check the results of this API you should use POSTMAN.
```
$ git clone https://github.com/elchoup/Django-API.git
$ pip install pipenv
$ cd API
$ pipenv install --requirements requirements.txt
$ pipenv shell
$ python manage.py runserver

```