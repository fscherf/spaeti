.PHONY: build


# app #########################################################################
.env: 
	cp example.env .env

server: .env
	docker compose up $(args)

migrate:
	docker compose exec app /app/scripts/manage.py migrate $(args)

collect-static:
	docker compose exec app /app/scripts/collect-static $(args)

createsuperuser:
	docker compose exec app /app/scripts/manage.py createsuperuser $(args)

build:
	docker compose build $(args)

# tests #######################################################################
test:
	docker compose run playwright tox $(args)

lint:
	docker compose run playwright tox -e lint $(args)

isort:
	docker compose run playwright tox -e isort $(args)
