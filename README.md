# Wolfeye API

![Wolfeye Logo](docs/logo.api.png)

This is the repository for the Wolfeye API.  
It is made to run with Traefik as a reverse proxy.

Currently hosted on https://wolfeye.jae.fi

## Local dev

This requires a Redis server listening in local.

Quickstart dev windows (using powershell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "main"
$env:FLASK_ENV = "development"
$env:REDIS_HOST = "localhost"
flask run
```

Quickstart dev linux:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP="main"
export FLASK_ENV="development"
export REDIS_HOST="localhost"
flask run
```
