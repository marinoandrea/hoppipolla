.PHONY: setup execute clean

setup:
	docker compose up &

execute: setup
	go run main.go

clean:
	docker compose down