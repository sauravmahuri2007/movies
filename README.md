# Movies (Django Movies Database)
A Django Pluggable Web App for Managing and Searching Movies like IMDB.

## Installation & Deployment Guide -

### 1. Install global dependencies

     sudo apt-get install virtualenv python-pip git mysql-server python3-dev gunicorn

### 2. Upgrade `pip` and `setuptools` that are bundled with the OS to the latest stable versions.

     sudo -H pip install pip -U

     sudo -H pip install setuptools -U

### 3. Clone the movies from github to your preferred directory (for example: '/home/ubuntu')

    git clone https://github.com/sauravmahuri2007/movies.git

    cd movies

### 4. Create virtualenv and install project dependencies

    virtualenv --python=python3 venv

    source venv/bin/activate

    pip install -r requirements.txt
    
### 5. Creating DB and setting up the tables my running the migrations

  1. Login to the preferred DBMS used for this application and create DB `movdb`
  For example, to create DB in mysql after login to console:
    
    create database movdb;
    
  2. Setting up the tables for movies:
    
    python manage.py migrate

  3. Creating superuser

    python manage.py createsuperuser


### 6. Run the app using the default lightweight Django web server (until this app is not part of a big application)

    python manage.py runserver

The app should have started running at http://127.0.0.1:8000.

### 7. systemd + gunicorn script for `movies` (For Ubuntu 16.04 and Higher):

  1. To let `systemd` handle running Movies/gunicorn, symlink the ready-to-use configuration file to `/etc/systemd/system/movies.service` —

        `sudo ln -s /home/ubuntu/movies/scripts/gunicorn.service /etc/systemd/system/movies.service`

    Once this is done, for auto-starting movies server after system reboots, enable it using —

        `sudo sudo systemctl enable movies`

  2. Simply start the job —

        `sudo systemctl start movies`

    To gracefully restart the app, you can use —

        `sudo systemctl restart movies`
