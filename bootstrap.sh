#!/bin/sh
#export FLASK_APP=./voucher/index.py
#export FLASK_APP=./voucher/index.py
#flask --debug run -h 0.0.0.0
gunicorn --bind 0.0.0.0:5000 wsgi:app
