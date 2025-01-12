## Welcome To GIFeels 
We have created a simple mood tracker to support mental health. As a guest you can see an inspirational quote or joke to improve your mindset. As a registered user you can log your moods, enter your thoughts in a journal and save your favourite jokes or quotes. You are also able to see a monthly overview of how you have been feeling.

This app is built with MYSQL, Python and Flask for the back-end. The front-end is built using Jinja, HTML, CSS and JavaScript

### You will need:

- A virtual environment on your IDE to install requirements from requirements.txt
- MySQL Workbench for the database (or equivalent)
- A developer API key from the [Giphy developers website](https://developers.giphy.com/)
- A developer OAuth account with Google cloud 


### Setup 
1. Create a new file at root level called .env. Copy and paste the template from [template_env](/template_env) and add your GIPHY API key, MySQL user and password where indicated. (Using .env will keep your personal information secure)
2. Create and activate a virtual environment, then install all requirements from [requirements.txt](/requirements.txt)
3. Run ['db_builder.py'](/database/db_builder.py). This will automatically run the queries needed to create and populate the database.
Another option for step 3:\
3. Using MYSQL Workbench create the database by running the query in [db_create.sql](/DB_Setup/db_create.sql).
4. Populate the database using the query in [db_populate.sql](/DB_Setup/db.populate.sql)

// CREATE DATABASE AND RUN DATABASE SCHEMA 
// SETUP SSL certificates 

### Running the app
By running app.py in your IDE you will be able to launch https://127.0.0.1:443 and go to the homepage of the app.

Please note: the front-end design has been optimised for Google Chrome Browser and for the best experience, we'd recommend using this.

The app will guide you through choosing how you feel and offer a choice for a joke or a quote. It will then allow you to add a journal entry.

You are able to visit the pages without logging into the app, however this will not allow you to save entries or have an overview of the recorded entries.

You can login as one of the mock users created, or register your own user following the instructions on screen.

### Mock users credentials
1. Mock user who is registered and has database entries from 01/05/2024 to 13/06/2024:\
Username: JoDoe\
Password: password123
2. Mock user who is registered only:\
Username: LSmith\
Password: hello123

### Developers

Laura: https://github.com/Laura-Kam \
Fabi: https://github.com/Fabi-P \
Rachel: https://github.com/Rachel-Tookey \
Alyssa: https://github.com/lyscodes \
Hannah: https://github.com/HannahTInsleyMcRink
