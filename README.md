Quickstart dev windows (using powershell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
$env:FLASK_APP = "main"
$env:FLASK_ENV = "development"
flask run
```

Quickstart dev linux:
```
pip install -r requirements.txt
export FLASK_APP="main"
export FLASK_ENV="development"
flask run
```
