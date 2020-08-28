
# Udacity Coffe Shop

## Introduction

This project was intended for the Full-Stack Developer Nanodegree program from Udacity. Udacity Coffee Shop is cafe system designed for its employees. It enables the baristas and managers to view the whole menu of the coffee shop, and allow the managers to set updates to the menu. The menu contains list of drinks, list of donuts, and list of combos, which is some drink and donut combo deals for the customers.


## Dependencies
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![Flask Versions](https://img.shields.io/badge/flask->=_1.0.3-blue)](https://pypi.org/project/Flask/)
[![Flask-SQLAlchemy Versions](https://img.shields.io/badge/Flask_SQLAlchemy->=_2.4.0-blue)](https://pypi.org/project/Flask-SQLAlchemy/) 
[![Gunicorn Versions](https://img.shields.io/badge/gunicorn-20.0.4-blue)](https://pypi.org/project/gunicorn/) 

To install all the dependencies for this project, run the following command 
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

You also need to download and install PostgreSQL from https://www.postgresql.org/ 

## Endpoints & Permissions

Allowed endpoints are as follow:

```python
- GET "/menu" 
    - to get the menu that contains a list of drinks, donuts and combos.
- GET "/combo"
    - to get the list of combos.
- POST "/drink"
    - to add a new drink to the menu.
- POST "/donut"
    - to add a new donut to the menu.
- POST "/combo"
    - to add a new combo to the menu.
- PATCH "/combo/<int:combo_id>"
    - to update a specific combo.
- DELETE "/combo/<int:combo_id>"
    - to delete a specific combo.
```

This application have two roles set to its users: **Barista** and **Manager**.<br> 
Barista have the following permissions:

- `get:menu`
- `get:combo`

While the manager have the following permissions:
- `get:menu`
- `get:combo`
- `post:drink`
- `post:donut`
- `post:combo`
- `patch:combo`
- `delete:combo`

## Local Running
To run this project locally, you need to make sure that the value of **ENV** is equal to `"dev"` in the following files:
1. `./auth.py` 
2. `./models.py`
3. `./auth/auth.py`

### Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Testing

To run a unit testing using `unittest`, simply run:
```
python3 test_app.py
```

## Production Running

This application is hosted in `heroku`, you can visit it by clicking [here](https://fsnd-capstone-hadeel.herokuapp.com/). Then follow these steps to interact with its endpoints: 

1. Log in as a **Barista**:
    - Email: barista@coffeeshop.com
    - Password: NroronAiAu6O
<br><br>or as a **Manager**:
    - Email: manager@coffeeshop.com
    - Password: jJpBF6w9eM64
2. Copy the token from the url after logging in.
3. Use the token to send requests to the API, using `curl` command or **Postman**.

Here some examples of a json body to send in your requests:

sending to `/drink` endpoint to add a new drink: 

```json
{
    "drink_title":"Milk"
}
```

sending to `/combo` endpoint to add a new combo: 

```json
{
    "drink_id": 1,
    "donut_id": 1   
}
```


## You have reached the end of this documentation, Thank You..






