FROM python:3.6
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get update -y
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
#RUN [ "python", "-c", "import nltk; nltk.download('all')" ]
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python installChilkat.py
# RUN python nltk_downloader.py
CMD python run.py


