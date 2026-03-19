inspect:
	fastmcp inspect ./app/server.py --format fastmcp

test:
	PYTHONPATH=app pytest app/tests/ -v

langchain:
	python3 app/langchain_client.py

seed:
	PYTHONPATH=app python3 app/modules/database/seed.py

docker-run:
	docker compose build
	docker compose run --rm app python app/langchain_client.py

docker-seed:
	docker compose build
	docker compose run --rm app python app/modules/database/seed.py
