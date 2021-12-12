Quickstart dev windows (using powershell):

  python -m venv venv
  .\venv\Scripts\Activate.ps1
  $env:FLASK_APP = "main"
  $env:FLASK_ENV = "development"
  flask run
