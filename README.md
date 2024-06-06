# cfg-group-4

## GIFeels 
A simple mood tracker.

#### You will need:

- MySQL Workbench for the database
- A developer API key from the [Giphy developers website](https://developers.giphy.com/)
- A virtual environment to install requirements from requirements.txt

#### Setup 
1. Config file: in [_config.py](/_config.py), add your GIPHY API key, MySQL user and password where indicated
2. Change the name from _config.py to config.py 
3. Create and activate a virtual environment, then install all requirements from [requirements.txt](/requirements.txt)
4. Create the database using the query in [db_create.sql](/DB_Setup/db_create.sql)
5. Populate the database using the query in [db_populate.sql](/DB_Setup/db.populate.sql)

#### Run the app
By running app.py in the terminal, you should be able to access the main page of the app.

The app will guide you through choosing how you feel and make a choice for a joke or a quote. It will then allow you to add a journal entry.
You are able to visit the pages without loggin into the app, however this will not allow you to save entries or have an overview of the recorded entries.

You can login as one of the mock users created, or register your own user following the instructions on screen.

#### Mock users credentials
1. username: JoDoe
    password: password123
2. username: LSmith
    password: hello123
