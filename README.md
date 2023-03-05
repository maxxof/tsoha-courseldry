Welcome to Courseldry

---

Courseldry is an app where university students can create reviews of the courses they have completed/attended to.
Here's what you can do in a final version of the app:

- Make an account, login, logout
- Read all the reviews that are stored in a database
- Engage with reviews (agree/disagree)
- Post a review
- Filter reviews by course name
- See each course's stats based on reviews
- Check user profile

---

Here's instructions on how to start the applicaton on your machine:

Clone this repository to your computer and move to the root directory of the application.
Create an `.env` file and paste following code there (NB: For some reason default port 
and/or host doesn't work properly on my machine so to avoid any complications I recommend
using these settings)

```
DATABASE_URL=<your-local-url>
SECRET_KEY=<some-random-numbers>
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8000
```
P.S Local url (postgre) is usually either `postgresql:///<database-name>` or `postgresql+psycopg2://`.

Then you create virtual environment and download app dependencies with commands

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Then define schema of your database

```
$ psql < schema.sql
```

Now you are ready to run the app:

```
$ flask run
```

---

Courseldry, 2023
