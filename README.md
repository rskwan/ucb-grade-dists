# UCB Grade Distributions

## Requirements

Python 2.7.x, Postgres, and the packages in `requirements.txt`.
Install the Python dependencies with `pip install -r requirements.txt`.

## Setup

* In Postgres, create a database for this. For example, if you wanted to call it `ucbgradedists`, run `CREATE DATABASE ucbgradedists`.
* Set these environment variables:
  * `DJANGO_SECRET_KEY`: a secret key (usually a randomly generated string)
  * `DJANGO_SETTINGS_MODULE`: use `ucbgradedists.settings.local` if you're in a development environment, and `ucbgradedists.settings.production` in production.
  * `DATABASE_URL`: a URL to your database. See the [dj_database_url](https://github.com/kennethreitz/dj-database-url) README for the format.
* Run `python manage.py migrate` to run the migrations and create tables for the models.
* Run `python manage.py importcsv [season] [year] [inname]` on a CSV file to import data. See `python manage.py importcsv -h` for more information.
* Run `python manage.py importdir [dir]` to import data from all CSV files in a directory.

## Current Functionality

* Importing grade distributions from Cal Answers CSV output.
* A RESTful API (via Tastypie) to access this data at `/api/v1/`. Check out [the Tastypie docs](http://django-tastypie.readthedocs.org/en/latest/) to figure out how to work with this!
* A very basic UI for accessing our data at `/search/subjects/`.

## TODO/Next Steps/The Future

* Add a data import page to the admin site.
* Introduce reasonable orderings for course numbers and grades.
* Improve the data viewer.
* Compute some interesting statistics.
* Make pretty graphs and apps and things.
* (Bonus) It would be cool to have a GUI for playing with the API.
* (Maybe) Create a model for Instructor (with a many-to-many field in Section), and parse it in the import script. (Problem: some instructors are distinct but have the same name.)

## License

This project is covered by the MIT License in `LICENSE.txt`.
