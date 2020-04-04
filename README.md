# SAP-service

Students and Professors feedback system for improving and analyzing of education process at university

## Run a project

Clone it
```
https://github.com/Unanoc/SAP-service.git
```
```
cd SAP-service/
```

Virtual environment
```
virtualenv venv
source /venv/bin/activate
pip3 install -r requirements.txt
```

Then change `config.json`. You need to get a telegram Token for your Telegram Bot.

Docker
```
docker-compose build
docker-compose up -d

docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```
