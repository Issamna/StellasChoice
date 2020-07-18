# Requirements
This app requires Python 3.7 or higher and pip for dependency control.
See requirements.txt for all Python dependencies for this project.
Some libraries have additional build dependencies.
* scikit-learn:
    * Cython >= 0.28.5
    * A C/C++ compiler and a matching OpenMP runtime library.
    * See https://scikit-learn.org/stable/developers/advanced_installation.html#platform-specific-instructions for more information depending on your platform.

# Installation Notes (Dev)
1. Clone project into your working directory
2. Create your virtual environment:
    * `/path/to/python3.7 -m venv /path/to/project_root/venv`
    * (Optional) If using Pycharm, add the new venv interpreter to project settings (Preferences -> Project -> Project Interpreter then select newly created interpreter to the list)
3. Ensure you're "sourced" into your virtual environment with source:
    * `/path/to/project_root/venv/bin/activate`
    * Your terminal should look something like `(venv) {machinename}:StellasChoice {user}`with `(venv)` prepending your typical console output
4. Install Python dependencies using:
    * `pip install -r /path/to/project_root/requirements.txt`
    * As stated above, some dependencies might have additional system requirements.
5. Create your Django migrations and SQLite database with the following Django commands:
    * `python manage.py makemigrations`
    * `python manage.py migrate`
6. Populate the database with the following:
    * `python manage.py TODO`
7. App can now be run with Django command:
    * `python manage.py runserver`

# Deployment Notes
The following are notes from deploying with Nginx/UWSGI on an AWS machine running Amazon Linux AMI. We are running UWSGI in "Emperor" mode

### UWSGI
See https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html for reference to UWSGI in Emperor mode

Installed UWSGI system-wide with the following command:
* `pip3.7 install uwsgi`

The command to run all deployable apps (including this one) is:
* `/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid ec2-user --gid ec2-user`

The settings for this app in particular are defined in `/etc/uwsgi/vassals/stellaschoice_uwsgi.ini` and the contents are as follows:
```
[uwsgi]
route-run = fixpathinfo:
project = stellaschoice
chdir = /var/www/vhosts/stellaschoice
home = /var/www/vhosts/stellaschoice/venv
module = stellachoice.wsgi:application

master = true
processes = 5

socket = /var/www/uwsgi/stellaschoice.sock
chown-socket = ec2-user:ec2-user
chmod-socket = 666
vacuum = true

touch-reload = /var/www/vhosts/stellaschoice/stellachoice/wsgi.py
```

Note: The touch-reload option will allow us to automatically redeploy the app to reflect new changes. Simply re-upload changes and use command `touch /var/www/vhosts/stellaschoice/stellachoice/wsgi.py` to automatically reload the application.

### Python:
#### Installation Details
* Project code lives in `/var/www/vhosts/stellaschoice`
* Virtual environment created at `/var/www/vhosta/stellaschoice/venv`

#### Steps
Create the virtual environment:
* `/usr/local/bin/python3.7 -m venv /var/www/vhosts/stellaschoic/venv`
 
Install required dependencies by entering the virtual environment then installing packages from our requirements.txt file:
 
* `source /var/www/vhosts/stellaschoic/venv/bin/activate`
* `pip install -r /var/www/vhosts/stellaschoice/requirements.txt`
  
Collect static files for Django to serve with the following Django command. This will compile all static components (CSS, JS, etc) to 

* `python /var/www/vhosts/stellaschoice/manage.py collectstatic`
  
(Optional) Run within virtual environment to make sure installation works correctly (site will be inaccessible but can check terminal for errors)
 
* `python /var/www/vhosts/stellaschoice/manage.py runserver`


### Nginx: 
The following is the relevant section of the Nginx server config. This will deploy the python app to `https://issamahmed.com/stellaschoice`. Nginx will serve the project's static files (JS, CSS, images) at `https://issamahmed.com/scstatic/*` 

```
location /stellaschoice {
  include /etc/nginx/uwsgi_params;
  uwsgi_pass unix:/var/www/uwsgi/stellaschoice.sock;
  uwsgi_param SCRIPT_NAME /stellaschoice;
}

location /scstatic {
  alias /var/www/vhosts/stellaschoice/scstatic; # Django static files
}
```

Then run the following to restart Nginx with the changes:

`sudo service nginx restart`