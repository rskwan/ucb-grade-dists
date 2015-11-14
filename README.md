# UCB Grade Distributions

A tool for exploration of grade distribution data obtained from Cal Answers.

## Requirements

Python 2.7.x, Postgres, and the packages in `requirements.txt`.

## Setup

### Local Development

* Create a virtualenv and install the Python dependencies with `pip install -r requirements.txt`.
* In Postgres, create a database for this. For example, if you wanted to call it `ucbgradedists`, run `CREATE DATABASE ucbgradedists`.
* Set these environment variables:
  * `DJANGO_SECRET_KEY`: a secret key (usually a randomly generated string)
  * `DJANGO_SETTINGS_MODULE`: use `ucbgradedists.settings.local` if you're in a development environment, and `ucbgradedists.settings.production` in production.
  * `DATABASE_URL`: a URL to your database. See the [dj_database_url](https://github.com/kennethreitz/dj-database-url) README for the format.
  * `ADMIN_NAME`, `ADMIN_EMAIL`: a name and email for the admin of the site.
  * `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Gmail user and password for the email to send from.
  * `SERVER_EMAIL`: the email that the server should send emails from (to admins/managers).
* Run `python manage.py migrate` to run the migrations and create tables for the models.
* Run `python manage.py importcsv [season] [year] [inname]` on a CSV file to import data. See `python manage.py importcsv -h` for more information.
* Run `python manage.py importdir [dir]` to import data from all CSV files in a directory.

### Deploying on Heroku

* Set up your app and dyno on Heroku:

        heroku create <your_app_name>
        git push heroku master
        heroku ps:scale web=1

* Set the environment variables listed above, either through Heroku's web interface, or with the CLI tool.
* Run `heroku run python ucbgradedists/manage.py migrate` to create the tables.
* (TODO) Eventually, we'll have an admin/superuser page to import CSV data.

## Functionality

### Current

* Importing grade distributions from Cal Answers CSV output.
* A RESTful API (via Tastypie) to access this data at `/api/v1/`. Check out [the Tastypie docs](http://django-tastypie.readthedocs.org/en/latest/) to figure out how to work with this!
* A basic UI for accessing our data at `/search/divisionsets/`.
  * We can browse data in terms of DivisionSets, which are sets of divisions (e.g. upper, lower, graduate) on which we compute subject-wide statistics.
  * This includes basic grade statistics -- average, standard deviation, median -- for each subject, course, and section. Thanks to DataTables, it's (mostly) sortable and searchable.

### Future

* Things that should be sortable, but aren't: terms, course/section numbers.
* (QUESTION) Which classes/subjects have the highest/lowest averages/medians/stdevs?
* (QUESTION) What do people think are the hardest/easiest (maybe say "highest/lowest grades") classes on campus? Within their major? How well does this match up with reality?
* Put a histogram (or similar chart) for each section (course? subject?).
  * The first two (section, course) are already covered by Berkeleytime and ScheduleBuilder for a lot of classes/terms, and it works pretty well.
  * Choice: grade points vs letter grades? We only use grade points in calculations, but maybe students care about A+ vs A- on their transcript.
* Calculate some statistics.
  * What percentile do you need to be at to get a certain letter grade, per section?
    * (Maybe) This could be useful for a course-level view, and interesting (if unhelpful) for a subject-level view.
  * (QUESTION) How different are distributions for lower vs upper vs graduate?
  * For a given subject, separate statistics by term: summer vs fall/spring.
    * (QUESTION) How different are summer grades from fall/spring grades?
    * (QUESTION, maybe) Are fall and spring grades different?
* Group by instructor.
  * (Maybe) Create a model for Instructor (with a many-to-many field in Section).
    * Problem: distinct people can have the same name.
* Trend of average (or median) over time, per course or subject (or instructor; see last bullet point).
* Track enrollment over time per course or subject.
  * For a course, maybe a bar for each term, divided up by instructor.
    * (QUESTION) Does enrollment correlate with grade distribution? Let's say average or median grade. The students don't know the grade distribution in advance, but they do know the instructor.
  * For a subject, a line chart of overall enrollment should be fine. A more fine-grained display that includes classes could be overkill and really cramped, unless there's a good way to do this.
* (Bonus) Add a data import page to the admin site.
* (Bonus) It would be cool to have a GUI for playing with the API. (Who knows if anyone is going to end up using it, though...)

## License

This project is covered by the MIT License in `LICENSE.txt`.
