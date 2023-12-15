<img align="right" src="https://github.com/ada-school/module-template/blob/main/ada.png">


## Python Data Mentor 👩‍💻 👨‍💻 Code Challenge

Thank you 🙏 for taking the time to implement this coding challenge to build a fast microservice REST API using *Python* and any other technologies of your preference.

## Conditions

* Take 2-4 hours to implement your project.
* Use coding best practices.
* Create a fork of this repo and share your solution when finished.


## Coding Challenge  💻 

A bus company wants to start using technology and allow their users to book online tickets. Please help them build a [REST API Level 2](https://martinfowler.com/articles/richardsonMaturityModel.html#level2)(pereferible) that lets them control their trip bookings, supporting the following operations:
* Create a new booking with the following information: name, email, origin, destination, departure date and time and duration.
* Update an existing booking
* Find a booking using its ID.
* Delete an existing booking.

# Expected Quality Attributes:
* Using coding best practices.
* SOLID principles.
* Correct connection with a persistance layer.

# Desired technology stack:
* Python 
* [Flask](https://flask.palletsprojects.com/en/2.2.x/) / [Fast API](https://fastapi.tiangolo.com/) / [Django](https://www.djangoproject.com/) / Any other
* MongoDB / Postgress / SQLite  / Any other

## Submit your solution

Once you're done, please send us an email to [tech@ada-school.org](mailto:tech@ada-school.org) with the subject: TECH_CHALLENGE_[YOUR NAME] and do not forget to include the link to your repository with the solution. After you submit your code, we will review it and contact you to discuss next steps. 

Good luck! 💪

# Solution

This is a web app version solution to the challenge

## Requirements to run the web app

1. Install the required packages in your python virtual env (venv, conda, etc.) by opening a terminal in the project folder and executing `pip install -r requirements.txt`

2. Create a Postgres database

3. Set up a `.env` file with the following lines:
    * `DB_URL=postgresql+psycopg://username:password@localhost:port/database`
    * `SECRET_KEY=YourSecretKey`
    * `ALGORITHM=HS256`
    * `ACCESS_TOKEN_EXPIRE_MINUTES=ExpTime`
    * `COOKIE_NAME=access_token`  
    Where you have to replace: 
    * `username`, `password`, `port` and `database` with actual username, password, port number and name of your postgres database
    * `YourSecretKey` with the key you want to use to create tokens, (you can generate one in linux with the command `openssl rand -hex 32`)
    * `ExpTime` with the time you want the session to last in minutes

## Using the web app

You can now test the web app, to do this:
1. Run the `main.py` file 
2. Click the URL showed in the terminal, it will open your browser
3. Now you can use the web app