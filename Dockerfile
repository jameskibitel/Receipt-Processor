# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /receipt-processor-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run unit tests before starting the Flask app
RUN python3 -m unittest discover -v

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]