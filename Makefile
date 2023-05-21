SHELL=/bin/bash
PYTHON=python3
PYTHON_ENV=env

# spaeti variables
DEBUG=1
SMTP_HOST=localhost
SMTP_PORT=1025

# django variables
DJANGO_SETTINGS_MODULE=spaeti._django.settings
DJANGO_DATABASE_NAME=db.sqlite3
DJANGO_STATIC_ROOT=spaeti/static/django

# lona variables
HOST=localhost
PORT=8080
LOG_LEVEL=info
SHELL_SERVER_URL=file://socket

.PHONY: all clean collectstatic server shell server-shell dist _release

all: | server

clean:
	rm -rf $(PYTHON_ENV)
	rm -rf $(DJANGO_STATIC_ROOT)

# python targets
$(PYTHON_ENV): pyproject.toml
	rm -rf $(PYTHON_ENV) && \
	$(PYTHON) -m venv $(PYTHON_ENV) && \
	. $(PYTHON_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .[dev]

shell: $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rlpython

smtp-server: $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	python -m smtpd -c DebuggingServer -n $(SMTP_HOST):$(SMTP_PORT)

# django targets
$(DJANGO_DATABASE_NAME): | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin migrate && \
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin createsuperuser

$(DJANGO_STATIC_ROOT): | $(PYTHON_ENV)
	rm -rf $(DJANGO_STATIC_ROOT) && \
	. $(PYTHON_ENV)/bin/activate && \
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin collectstatic $(args)

# lona targets
server: $(PYTHON_ENV) | $(DJANGO_DATABASE_NAME) $(DJANGO_STATIC_ROOT)
	. $(PYTHON_ENV)/bin/activate && \
	SPAETI_DEBUG=$(DEBUG) lona run-server \
		--project-root=spaeti \
		-s settings.py \
		--host $(HOST) \
		--port $(PORT) \
		--log-level=$(LOG_LEVEL) \
		--shell-server-url=$(SHELL_SERVER_URL) \
		$(args)

server-shell: $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rlpython $(SHELL_SERVER_URL) $(args)

# test targets
test:
	docker-compose run playwright tox $(args)

lint:
	docker-compose run playwright tox -e lint $(args)

isort:
	docker-compose run playwright tox -e isort $(args)

# packaging targets
dist: | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	python -m build

_release: dist
	. $(PYTHON_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*
