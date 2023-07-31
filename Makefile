# app #########################################################################
server:
	docker compose up $(args)

restart-app:
	docker compose restart app --no-deps

migrate:
	docker compose exec app ./docker-entrypoint.sh migrate $(args)

migrations:
	docker compose exec app ./docker-entrypoint.sh makemigrations spaeti $(args)

superuser:
	docker compose exec app ./docker-entrypoint.sh createsuperuser $(args)

# tests #######################################################################
test:
	docker compose run playwright tox $(args)

lint:
	docker compose run playwright tox -e lint $(args)

isort:
	docker compose run playwright tox -e isort $(args)
