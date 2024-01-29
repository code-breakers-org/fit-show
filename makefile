
ifneq ("$(wildcard .env)","")
    include .env
endif
CHANGED_FILES := git diff --name-only --diff-filter=d | grep -E "\.py$$" | tr "\n" " "
FILES := $(shell $(CHANGED_FILES))

DBDOCS_FILENAME = database.dbml

ARG1 := $(word 2, $(MAKECMDGOALS) )
ARG2 := $(word 3, $(MAKECMDGOALS) )
ARG3 := $(word 4, $(MAKECMDGOALS) )

githook:
	@ git config --local core.hooksPath .githooks/

run-dev:
	python manage.py runserver 0.0.0.0:$(DJANGO_PORT)

run:
	python manage.py runserver 0.0.0.0:$(DJANGO_PORT)

pip:
	pip install -r ./requirements/production.txt

pip-dev:
	pip install -r ./requirements/local.txt

pip-update-dev:
	pip install -U -r requirements/local.txt

test:
	python manage.py test

format:
	black **/*.py --exclude '\.venv/|\.git/'

format-check:
	black **/*.py --check --exclude '\.venv/|\.git/'

lint:
	pylint --recursive=y .

lint-changed-files:
	@echo "Linting Python files:"
	@if [ -n "$(FILES)" ]; then \
		pylint --recursive=y $(FILES); \
	else \
		echo "No Python files to lint."; \
	fi
install-dbdocs:
	npm install -g dbdocs
	dbdocs login

initial-dbdocs:
	dbdocs build $(DBDOCS_FILENAME)

