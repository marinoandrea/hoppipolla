.PHONY: setup execute clean

setup:
	docker compose up

execute: setup
	go main.go

clean:
	docker compose down