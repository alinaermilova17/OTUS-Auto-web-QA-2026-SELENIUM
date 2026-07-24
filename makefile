.PHONY: build test test-chrome test-firefox test-headed clean up down logs

up:
	docker-compose up -d

down:
	docker-compose down -v

build:
	docker build -t tests .

test: build
	docker-compose run --rm tests

test-chrome:
	docker-compose run --rm tests --browser=chrome

test-firefox:
	docker-compose run --rm tests --browser=firefox

test-headed:
	docker-compose run --rm tests --headed

test-specific:
	docker-compose run --rm tests $(TEST_PATH)

logs:
	docker-compose logs -f

shell:
	docker-compose run --rm tests /bin/bash

clean:
	docker-compose down -v
	docker rmi tests || true
	docker system prune -f || true