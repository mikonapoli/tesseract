init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run mypy .
	pipenv run nosetests

accept:
	pipenv run behave
