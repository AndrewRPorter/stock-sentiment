FROM python:3.6-slim

ENV PROJECT=stock-sentiment
ENV CONTAINER_HOME=/opt
ENV CONTAINER_PROJECT=$CONTAINER_HOME/$PROJECT

WORKDIR $CONTAINER_PROJECT

COPY . $CONTAINER_PROJECT

COPY start.sh /start.sh
COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r /requirements.txt

RUN python -m textblob.download_corpora

EXPOSE 8000

CMD ["/start.sh"]
