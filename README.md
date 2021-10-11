# FlaslBase
Basic flask rest api with user authentication

## Get started

### Docker
You can get it up and running with docker by simply:

`sudo docker-compose up`

### Locally/Manually
or if you want to run it locally, I recommend setting up a virtual environment first
```
python -m virtualenv venv
pip install -r requirements.txt
```

Make sure to change the .env file to your local postgresql and migrate the models

`flask db upgrade`

Get swagger-ui up and running: [Swagger-ui](https://swagger.io/docs/open-source-tools/swagger-ui/development/setting-up/)

and finally go ahead and start the flask app simply by

`python manager.py runserver --host 0.0.0.0 --port 5000 --debug`
