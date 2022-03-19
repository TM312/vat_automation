run-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

run-dev-d:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

init-db:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec api python manage.py db init

seed-db:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec api python manage.py seed_db