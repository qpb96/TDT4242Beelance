# beelance

## Code and structure

.gitlab-ci.yml - gitlab ci
Procfile - heroku kjører serveren

- **beelance/** django project folder containing the projects modules
  - **core/** contains all the projects tamplates
    - **index.html** One of the projects templates that uses a template language to insert if, loops and variables into html.
  - **home/** user profile - overview over user projects
    - **static/** - contains static files like js and images
    - **templatetags/** folder containing [template tags](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/). Methods you import into your templates. Can be used in combination with views.
    - **admins.py** - file contaning defenitions to connect models to the django admin panel
    - **urls.py** - contains mapping between urls and views
    - **models.py** - contains data models
    - **tests/** - contains tests for the module. [View Testing in Django](https://docs.djangoproject.com/en/2.1/topics/testing/) for more.
    - **views.py** - Controller in MVC. Methods for redering and accepting user data
    - **forms.py**  -  defenition of forms. Used to render html forms and verify user input


  **payment/** - module handeling payment
  **projects/** - The largest module of the project containing code for creating project and tasks. Upload files, view files, adding roles and user to roles.
  - **beelance/** - The projects main module contaning settings.
  - **static/** - common static files
  - **user/** - module extending djangos user model with a profile contaning more information about the user.
  - **manage.py** - entry point for running the project.
  - **seed.json** - contains seed data for the project to get up and running quickly



## Know beelance security problems
 - no https
 - you can grant access to a file to a team that is not on the task
 - Delete files have no authorization
 - file types and content is not checked
 - upload files can be viwed by anyone who has the url.


## Get started
It's reccomended to have a look at: https://www.djangoproject.com/start/

Basic tutorial that walks trough what the different files does.
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

Create a virtualenv https://docs.python-guide.org/dev/virtualenvs/


## Local setup

### Installation with examples for ubuntu. Windows and OSX is mostly the same

Fork the project and clone it to your machine.

#### Setup and ctivation of virtualenv (env that prevents python packages from being installed globaly on te machine)

`pip install virtualenv`

`virtualenv env`

`source env/bin/activate`


#### Install python requirements

`pip install -r requirements.txt`


#### Migrate database

`python manage.py migrate`


#### Create superuser

Create a local admin user by entering the following command:

`python manage.py createsuperuser`

Only username and password is required


#### Start the app

`python manage.py runserver`


#### Add initial data

Add initial data go to the url the app is running on localy after `runserver` and add `/admin` to the url.

Add some categories and you should be all set.

or by entering

`python manage.py loaddata seed.json`


## Email
Copy `beelance/local_settings_example.py` to `beelance/local_settings.py` and replace the email placeholder values with values dscribes in the email beelancetion later in the instructions.

To support sending of email you will have to create a gmail account and turn on less beelanceure apps. *Do not use your own email as Google might lock the account*. See https://support.google.com/accounts/answer/6010255?hl=en for instructions for turning on less beelanceure apps.

To get mail working on heroku you might have to visit https://accounts.google.com/DisplayUnlockCaptcha and click `continue` as the heroku server is in another location and Google thinks it is a hacking atempt. 

## Continuous integration
Continuous integration will build the code pushed to master and push it to your heroku app so you get a live version of your latest code by just pushing your code to GitLab.

1. Create heroku account and a app.
2. Set the project in the .gitlab-cs.yml file by replace `<You-herokupoject-name>` with the name of the Heroku app you created
`- dpl --provider=heroku --app=<You-herokupoject-name> --api-key=$HEROKU_STAGING_API_KEY`
3. Fork the project at GitLab
4. Set varibles at GitLab
    * settings > ci > Variables
    * `HEROKU_STAGING_API_KEY` = heroku > Account Settings > API Key
4. Add heroku database
   * Resrouces > Add ons > search for postgres > add first option
5. Set variables at heroku. Settings > Config vars > Reveal vars
   * `DATABASE_URL` = Should be set by default. if not here is where you can find it: Resources > postgress > settings > view credentials > URI
   * `DISABLE_COLLECTSTATIC` = `1`  collectio nof static resources fails and is therefore disabled
   * `EMAIL_HOST_PASSWORD` mail password. Not mandatory if you do not want to send email
   * `EMAIL_HOST_USER` mail adress. Not mandatory if you do not want to send email
   * `IS_HEROKU` = `IS_HEROKU`
6. On GitLab go to CI / CD in the reposotry meny and select `Run Pipeline` if it has not already started. When both stages compleets the app should be available on heroku. Staging will fail from timeout as Heroku does not give the propper response to end the job. But the log should state that the app was deployed.
7. Setup the applications database.
  * Install heroku CLI by following: https://devcenter.heroku.com/articles/heroku-cli
  * Login in the Hroku CLI by entering `heroku login`. This opens a webbrowser and you accept the login request.
  * Migrate database by entering
  `heroku run python manage.py migrate -a <heroku-app-name>`. `Heroku run` will run the folowing command on your heroku instance. remember to replace `<heroku-app-name>` with your app name
  * and create a admin account by running
  `heroku run python manage.py createsuperuser -a <heroku-app-name>`.
  * seed database `heroku run python manage.py `

### Reset Database
`heroku pg:reset DATABASE_URL -a <heroku-app-name>`

## Data seeding
The data seed provided contains 3 users:

Username | Password | Description
---|---|---
admin|qwerty123|Admin user that owns one project
harrypotter|qwerty123|
joe|qwerty123|
