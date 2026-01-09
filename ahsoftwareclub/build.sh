#!/usr/bin/env bash
set -o errexit

export DEBUG="False"

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate