init:
	pip install pipenv
	pipenv install --dev

test:
	export MYPYPATH=$$PWD/tesseract; pipenv run mypy .
	pipenv run nosetests

accept:
	pipenv run behave

run:
	pipenv run python tesseract/Tesseract.py
