How to set up new site
=====================
## Libraries 
* nginx
* python
* venv + pip
* git

in Unix:
sudo apt-get install nginx git python python-venv

## Configure nginx

* look to: nginx.template.conf
* change SITENAME to staging.my-domain.com

## Configure systemd

* look to: gunicorn-systemd.template.service
* change SITENAME to staging.my-domain.com

## Project structure

/home/username/sites/SITENAME:
* database
* src
* static
* venv
