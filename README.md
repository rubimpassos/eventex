# Eventex
Event landing page developed in Welcome to the Django

[![Build Status](https://travis-ci.org/rubimpassos/eventex.svg?branch=master)](https://travis-ci.org/rubimpassos/eventex)
[![Code Health](https://landscape.io/github/rubimpassos/eventex/master/landscape.svg?style=flat)](https://landscape.io/github/rubimpassos/eventex/master)


## Getting Started

1. Clone this repository
2. Install Python 3.5+ and create a virtualenv
3. Activate the virtualenv
4. Install the dependencies
5. Configure .env instance
6. Run the tests

```console
git clone https://github.com/rubimpassos/eventex eventex
cd eventex
python -m venv .eventex
source .eventex/Scripts/activate.bat
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```

## Deployment

1. Create a app in Heroku
2. Send the config to heroku
3. Define a secure secret key in heroku config vars
4. Define DEBUG=False
5. Configure an email service(e.g SendGrid)
6. Push to heroku

```console
heroku create myapp
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# configure a email service that you like
git push heroku master --force
```