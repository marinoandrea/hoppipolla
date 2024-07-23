include .env

SHELL := /bin/bash

scenario = "$(shell pwd)"

.PHONY: setup execute clean

setup: topology.topo scenario.py hoppipolla.ini data/geography.template.json policies/main.template.lp
	python3 -m venv .venv; \
		source .venv/bin/activate; \
		python -m pip install --upgrade pip; \
		pip install python-dotenv networkx pyyaml plumbum toml; \
		cd ${HOPPIPOLLA_SCION_HOME}; \
			./scion.sh topology -d -c ${scenario}/topology.topo; \
			./scion.sh run; \
		cd ${scenario}; \
			pip install -e ../../sdks/python; \
			python ../utils/populate_templates.py -s ${scenario}

	cd ${HOPPIPOLLA_SCION_HOME}; \
		export HOPPIPOLLA_SCIOND_URI=$(./scion.sh sciond-addr 111); \
	cd ${scenario};
		docker compose build

execute: 
	trap "docker compose stop" EXIT; \
		docker compose up -d; \
		source .venv/bin/activate; \
			python scenario.py

clean:
	docker compose down

	source .venv/bin/activate; \
		rm policies/main.lp
		rm data/geography.json
		cd ${HOPPIPOLLA_SCION_HOME}; \
			./scion.sh topology -d -c ${scenario}/topology.topo; \
			./scion.sh run

	rm -rf .venv