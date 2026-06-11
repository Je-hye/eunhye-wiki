.PHONY: up down config test-api test-boundaries test

up:
	docker compose up --build

down:
	docker compose down

config:
	docker compose config --quiet

test-api:
	docker compose run --rm public-api python -m unittest discover -s tests

test-boundaries:
	python3 -m unittest discover -s tests

test: config test-api test-boundaries
