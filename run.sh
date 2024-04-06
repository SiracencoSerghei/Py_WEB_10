#!/bin/sh

echo Sleep 2...
sleep 2
cd hw_10
python manage.py migrate
echo Sleep 2...
sleep 2
python manage.py runserver 0.0.0.0:8000

