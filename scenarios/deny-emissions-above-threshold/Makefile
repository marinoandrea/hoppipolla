include .env

scenario = "$(shell pwd)"

.PHONY: scion setup clean

.ONESHELL:

.PHONY: setup execute clean

setup: topology.topo scenario.py hoppipolla.ini data/geography.template.json policies/main.template.lp
	cd ${HOPPIPOLLA_SCION_HOME}; \
		./scion.sh topology -c ${scenario}/topology.topo; \
		./scion.sh run

	python3 -m venv .venv; \
		source .venv/bin/activate; \
		python -m pip install --upgrade pip; \
		pip install networkx; \
		pip install -e ../../sdks/python; \
		python3 ../utils/populate_templates.py -s ${scenario}; \
		python3 ../utils/generate_energy_readings.py -s ${scenario}

execute: 
	function tearDown {
		docker compose down
	}
	trap tearDown EXIT
	docker compose up -d
	source .venv/bin/activate; \
		python scenario.py

clean:
	rm -rf .venv
	rm policies/main.lp
	rm data/energy.json