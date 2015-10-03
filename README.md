# UCB Grade Distributions

## Requirements

Python 2.7.x, Postgres, and the packages in `requirements.txt`.
Install the dependencies with `pip install -r requirements.txt`.

## Setup

* Create a `ucbgradedists` database in Postgres.
* Set these environment variables:
  * `DJANGO_SECRET_KEY`: a secret key (usually a randomly generated string)
  * `DJANGO_SETTINGS_MODULE`: use `ucbgradedists.settings.local` if you're in a development environment, and `ucbgradedists.settings.production` in production.
* Run `python manage.py migrate` to run the migrations and create tables for the models.
* Run `python manage.py importcsv [season] [year] [inname]` on a CSV file to import data. See `python manage.py importcsv -h` for more information.

## License

This project is covered by the MIT License in `LICENSE.txt`.
