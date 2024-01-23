CHANGED_FILES = git diff --name-only --diff-filter=d | grep -E "\.py$" | tr "\n" " "
PROJECT_NAME = "fit_show"
ARG1 := $(word 2, $(MAKECMDGOALS) )
ARG2 := $(word 3, $(MAKECMDGOALS) )
ARG3 := $(word 4, $(MAKECMDGOALS) )

githook:
	@ git config --local core.hooksPath .githooks/

update:
	@ $(PIP_BIN) install -r requirements/local.txt

run-dev:
	python manage.py runserver 0.0.0.0:8000

run:
	python manage.py runserver 0.0.0.0:8000

pip:
	pip install -r ./requirements/production.txt

pip-dev:
	pip install -r ./requirements/local.txt

test:
	python manage.py test

format:
	black **/*.py --exclude '\.venv/|\.git/'

format-check:
	black **/*.py --check --exclude '\.venv/|\.git/'

lint:
	pylint --recursive=y .

lint-changed-files:
	FILES=$("$CHANGED_FILES") && [[ ! -z "$(FILES)" ]] && pylint --recursive=y "$(FILES)" || echo ""

install-dbdocs:
	npm install -g dbdocs

initial-dbdocs:
	dbdocs login
	dbdocs build database.dbml --project= $(PROJECTNAME)
