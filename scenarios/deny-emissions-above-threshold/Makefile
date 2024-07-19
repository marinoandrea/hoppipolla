include .env

scenario = "$(shell pwd)"

.PHONY: scion setup clean

scion: topology.topo
	cd ${HOPPIPOLLA_SCION_HOME}; \
		./scion.sh topology -c ${scenario}/topology.topo; \
		./scion.sh run

setup:
	python3 ../utils/populate_templates.py -s ${scenario}
	python3 ../utils/generate_energy_readings.py -s ${scenario}

clean:
	rm policies/main.lp
	rm data/energy.json