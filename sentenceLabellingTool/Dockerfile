FROM python:3.6
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get update -y
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python installChilkat.py
CMD python run.py 0.0.0.0 -p 5005
