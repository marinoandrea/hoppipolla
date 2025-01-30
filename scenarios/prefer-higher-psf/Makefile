.PHONY: setup execute clean

setup:
	HOPPIPOLLA_NIP_PROXY_LOCAL_JSON=nip.json docker compose up

execute: setup
	go main.go

clean:
	docker compose down