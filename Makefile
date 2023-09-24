migrate:
	python manage.py migrate

local:
	python manage.py runserver

up-inv:
	docker build -t invoicing:localinvoicing .

inv:
	docker-compose up -d --remove-orphans
	@docker ps
	@docker exec -it localinvoicing bash