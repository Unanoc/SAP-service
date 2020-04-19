venv=venv/bin/

init:
	make pyenv
	make db

pyenv:
	(test -d ${PWD}/venv || virtualenv ${PWD}/venv); \
	source ${PWD}/venv/bin/activate && \
	pip3 install --no-cache-dir -U pip && \
	pip3 install --no-cache-dir -r ${PWD}/requirements.txt;

db:
	find . -type f -name db.sqlite3 -delete
	touch db.sqlite3
	find application/sap/migrations/ -type f -name "[^__]*[^__].py" -delete
	$(venv)python manage.py makemigrations
	$(venv)python manage.py migrate

fake-gen:
	$(venv)python manage.py fake_generator

run:
	$(venv)python manage.py runserver 0.0.0.0:8000

clean:
	# __pycache__, *.pyc, *.pyo
	find . | grep -E "__pycache__|\.pyc|\.pyo" | xargs rm -rf
	# venv
	find . | grep -E "venv|mysql" | xargs rm -rf
	# db.sqlite3
	find . -type f -name db.sqlite3 -delete
	# application/sap/migrations/*
	find application/sap/migrations/ -type f -name "[^__]*[^__].py" -delete 

# Docker
docker:
	docker-compose up -d db
	docker-compose run web python manage.py makemigrations
	docker-compose run web python manage.py migrate
	docker-compose up -d web

docker-stop:
	docker-compose stop

docker-clean:
	make docker-stop
	docker rm $$(docker ps -a | grep -E "sap-service*" | awk '{print $$1}')
	docker rmi $$(docker images | grep -E "mysql|sap-service*" | awk '{print $$3}')
	# mysql
	find . | grep -E "venv|mysql" | xargs rm -rf

# Internalization
messages:
	django-admin.py makemessages -l ru -i "django*"

compile:
	django-admin.py compilemessages

# admin
superuser:
	python manage.py createsuperuser