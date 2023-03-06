venv:
	rm -rf venv
	python3 -m venv venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install -U -r requirements.txt

test: venv
	./venv/bin/pytest tests --junitxml=report.xml

coverage: venv
	./venv/bin/pytest --verbose --cov-report term --cov-report xml --cov=chomp tests

lint: venv
	./venv/bin/black chomp tests

clean:
	rm -rf venv

build:
	python3 -m build
