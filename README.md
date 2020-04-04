# SAP-service

<p align="center">
  <a href="#"><img src="https://github.com/Unanoc/SAP-service/blob/master/media/default/default_avatar.png" alt="SAP"></a>
</p>

Students and Professors feedback system for improving and analyzing of education process at university

## Run a project

### Download a project.
```
git clone https://github.com/Unanoc/SAP-service.git
cd SAP-service/
```

Then, change `config.json`: 
- You need to get a Telegram token for your Telegram Bot and replace it in `config.json`;
- Set `true` for "prod" in `config.json`;

### Docker container
```
docker-compose up -d db
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up -d web
```

## Local environment

### Download a project.
```
git clone https://github.com/Unanoc/SAP-service.git
cd SAP-service/
```

### Virtual environment
```
virtualenv venv && source venv/bin/activate && pip3 install -r requirements.txt
```

Then, change `config.json`: 
- You need to get a Telegram token for your Telegram Bot and replace it in `config.json`;
- Set `false` for "prod" in `config.json`;

```
./recreate_db.sh
python manage.py runserver 0.0.0.0:8000
```

### Generate fake data
```
python manage.py fake_generator
```