FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install build-essential git libncurses-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get purge -y --auto-remove build-essential git libncurses-dev

COPY . .

ENV FLASK_APP="main"
ENV FLASK_ENV="production"

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
