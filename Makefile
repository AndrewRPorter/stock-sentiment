all: clean train test build docker-run

run:
	python3 run.py

deploy:
	gunicorn --bind 0.0.0.0:8000 --workers 4 app.wsgi

docker-run:
	sudo docker build -t dev/stock-sentiment .
	sudo docker run -it -p 8000:8000 dev/stock-sentiment

test: train
	python3 -m pytest -rav tests

train-web:
	python3 app/sentiment/train-web/run.py

train:
	python3 -m textblob.download_corpora
	python3 app/sentiment/train.py

clean:
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf ./instance
	rm app/sentiment/classifier.pickle

.PHONY: clean train test build docker-run run all
