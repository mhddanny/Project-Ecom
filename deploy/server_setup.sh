#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/mhddanny/Project-Ecom.git'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/projectCart

mkdir -p $VIRTUALENV_BASE_PATH
python3 -m venv $VIRTUALENV_BASE_PATH/projectCart

$VIRTUALENV_BASE_PATH/projectCart/bin/pip install -r $PROJECT_BASE_PATH/projectCart/requirements.txt

# Run migrations
cd $PROJECT_BASE_PATH/projectCart/src

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/projectCart/deploy/supervisor_projectCart.conf /etc/supervisor/conf.d/projectCart.conf
supervisorctl reread
supervisorctl update
supervisorctl restart projectCart

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/projectCart/deploy/nginx_projectCart.conf /etc/nginx/sites-available/projectCart.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/projectCart.conf /etc/nginx/sites-enabled/projectCart.conf
systemctl restart nginx.service

echo "DONE! :)"