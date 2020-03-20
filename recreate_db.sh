# !/bin/sh

find . -type f -name db.sqlite3 -delete
touch db.sqlite3

find application/sap/migrations/ -type f -name "[^__]*[^__].py" -delete

python manage.py makemigrations
python manage.py migrate