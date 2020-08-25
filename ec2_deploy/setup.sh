#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/jigneshkotadiya000/explore_graphene_django.git'

PROJECT_BASE_PATH='/usr/local/apps/explore_graphene_django'

echo "Installing dependencies..."

sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa
sudo apt-get update
sudo apt install -y python3.7
sudo apt-get install -y python3.7-dev python3.7-venv sqlite python-pip supervisor nginx git python-mysqldb libmysqlclient-dev


# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3.7 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Configure supervisor
cp $PROJECT_BASE_PATH/ec2_deploy/supervisor_explore_graphene_django.conf /etc/supervisor/conf.d/explore_graphene_django.conf
supervisorctl reread
supervisorctl update
supervisorctl restart explore_graphene_django

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure nginx
cp $PROJECT_BASE_PATH/ec2_deploy/nginx_explore_graphene_django.conf /etc/nginx/sites-available/explore_graphene_django.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/explore_graphene_django.conf /etc/nginx/sites-enabled/explore_graphene_django.conf
systemctl restart nginx.service

echo "DONE! :)"
