#!/usr/bin/env python3
'''
This script is a utility tool for the Hoppipolla framework developers and
testers that allows to generate energy readings in a format that can be used
by the NIP proxy in its mocking mode.
'''
import json
import logging
import os
import random
import sys
import uuid
from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable, TypedDict

from common import parse_ini_file, parse_topology_file


@dataclass
class Config:
    start: datetime
    end: datetime
    delta_mins: int = 1
    random_seed: int = 1
    probability_status_switch: float = 0.1
    n_machines_per_as: int = 10

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Generation start time cannot be after end time")


@dataclass(frozen=True)
class ProgramArguments:
    scenario: str
    debug: bool


def parse_arguments() -> ProgramArguments:
    parser = ArgumentParser(
        prog="[Hoppipolla] Energy Readings Generation Tool",
        description="A CLI for generating artifical energy readings for an AS",
        epilog="This is part of the Hoppipolla framework (https://github.com/marinoandrea/hoppipolla)"
    )

    parser.add_argument(
        "-s", "--scenario",
        type=str,
        help="File path to the scenario folder"
    )
    parser.add_argument(
        "--debug",
        action="store_true"
    )

    args = parser.parse_args(sys.argv[1:])

    return ProgramArguments(scenario=args.scenario, debug=args.debug)


def generate_seeded_uuid() -> str:
    return str(uuid.UUID(int=random.getrandbits(128), version=4))


ENERGY_RATINGS = ['A++', 'A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
POWER_SOURCES = ["grid", "battery", "solar", "eolic", "hydro"]
MACHINE_STATUSES = ["idle", "operational", "maintenance", "off"]


@dataclass
class Machine:
    isd_as: str
    id: str = field(default_factory=generate_seeded_uuid)
    current_status: str = field(
        default_factory=lambda: random.choice(MACHINE_STATUSES))
    current_source: str = field(
        default_factory=lambda: random.choice(POWER_SOURCES))
    energy_rating: str = field(
        default_factory=lambda: random.choice(ENERGY_RATINGS))


class BaseReading(TypedDict):
    id: str
    isdAs: str
    collectedAt: str  # ISO formatted timestamp
    machineId: str
    energyEfficiencyRating: str
    status: str


class EnergyReading(BaseReading):
    energyConsumptionKwh: float
    cpuUsagePercentage: float
    memoryUsagePercentage: float
    networkTrafficMB: float
    temperatureCelsius: float
    carbonEmissionsKg: float
    renewableEnergyPercentage: float


def generate_reading(config: Config, machine: Machine, timestamp: datetime) -> EnergyReading:
    switch_status = random.random() > config.probability_status_switch

    base_data: BaseReading = {
        "id": generate_seeded_uuid(),
        "isdAs": machine.isd_as,
        "collectedAt": timestamp.isoformat(),
        "machineId": machine.id,
        "energyEfficiencyRating": machine.energy_rating,
        "status": random.choice(MACHINE_STATUSES) if switch_status else machine.current_status,
    }

    if base_data["status"] == "off":
        return {
            **base_data,
            "carbonEmissionsKg": 0.0,
            "cpuUsagePercentage": 0.0,
            "energyConsumptionKwh": 0.0,
            "memoryUsagePercentage": 0.0,
            "networkTrafficMB": 0.0,
            "renewableEnergyPercentage": random.random() * 100.0,
            "temperatureCelsius": random.uniform(10.0, 40.0),
        }

    elif base_data["status"] == "maintenance":
        return {
            **base_data,
            "carbonEmissionsKg": random.random() * 50.0,
            "cpuUsagePercentage": random.uniform(0.0, 50.0),
            "memoryUsagePercentage": random.uniform(0.0, 50.0),
            "energyConsumptionKwh": random.random() * 200.0,
            "networkTrafficMB": random.random() * 50000.0,
            "renewableEnergyPercentage": random.random() * 100.0,
            "temperatureCelsius": random.uniform(10.0, 60.0),
        }

    elif base_data["status"] == "idle":
        return {
            **base_data,
            "carbonEmissionsKg": random.random() * 10.0,
            "cpuUsagePercentage": random.uniform(0.0, 10.0),
            "memoryUsagePercentage": random.uniform(0.0, 20.0),
            "energyConsumptionKwh": random.uniform(0.5, 50.0),
            "networkTrafficMB": random.random() * 1000.0,
            "renewableEnergyPercentage": random.random() * 100.0,
            "temperatureCelsius": random.uniform(10.0, 40.0),
        }

    return {
        **base_data,
        "carbonEmissionsKg": random.random() * 100.0,
        "cpuUsagePercentage": random.random() * 100.0,
        "energyConsumptionKwh": random.uniform(1.0, 1000.0),
        "memoryUsagePercentage": random.uniform(10.0, 100.0),
        "networkTrafficMB": random.random() * 100000.0,
        "renewableEnergyPercentage": random.random() * 100.0,
        "temperatureCelsius": random.uniform(20.0, 80.0),
    }


def generate_readings(config: Config, isd_ases: Iterable[str]):
    readings: dict[str, list[EnergyReading]] = {}

    for isd_as in isd_ases:
        if isd_as not in readings:
            readings[isd_as] = []

        machines: list[Machine] = [
            Machine(isd_as=isd_as) for _ in range(config.n_machines_per_as)]

        current_timestamp = config.start
        while current_timestamp != config.end:
            for machine in machines:
                reading = generate_reading(config, machine, current_timestamp)
                readings[isd_as].append(reading)
            current_timestamp += timedelta(minutes=config.delta_mins)

    return readings


def main() -> None:
    args = parse_arguments()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='[%(levelname)s]: %(message)s',
    )

    config_ini = parse_ini_file(args.scenario)
    config_ini_generation = config_ini["generation.data.energy"]

    try:
        config = Config(
            start=datetime.fromisoformat(config_ini_generation["Start"]),
            end=datetime.fromisoformat(config_ini_generation["End"]),
        )
        if "DeltaMins" in config_ini_generation:
            config.delta_mins = int(config_ini_generation["DeltaMins"])
        if "RandomSeed" in config_ini_generation:
            config.random_seed = int(config_ini_generation["RandomSeed"])
        if "NMachinesPerAs" in config_ini_generation:
            config.n_machines_per_as = int(config_ini_generation["NMachinesPerAs"])
        if "ProbabilityStatusSwitch" in config_ini_generation:
            config.n_machines_per_as = int(config_ini_generation["ProbabilityStatusSwitch"])
    except ValueError as e:
        logging.error(str(e))
        exit(1)

    logging.info(
        f"Data generation interval is [{config.start.isoformat()},{config.end.isoformat()}]")

    random.seed(config.random_seed)
    logging.info(f"Using randomization seed={config.random_seed}")

    logging.info(
        f"Probability for a machine to switch status is {config.probability_status_switch}")

    try:
        logging.info("Parsing topology file")
        graph = parse_topology_file(f"{args.scenario}/topology.topo")
        isd_ases = set(node for node in graph.nodes)
    except ValueError as e:
        logging.error(str(e))
        exit(1)

    if len(isd_ases) == 0:
        logging.error("No ASes found in the topology file")
        exit(1)

    logging.info(f"Found ASes: {', '.join(isd_ases)}")

    n_readings_per_machine = int(
        (config.end - config.start).total_seconds() / 60 / config.delta_mins)
    logging.info(f"Generating {n_readings_per_machine} readings per machine")

    n_readings_per_as = n_readings_per_machine * config.n_machines_per_as
    logging.info(f"Generating {n_readings_per_as} readings per AS")

    n_readings_total = n_readings_per_as * len(isd_ases)
    logging.info(f"Generating total of {n_readings_total} readings")

    readings = generate_readings(config, isd_ases)

    output = f"{args.scenario}/data/energy.json"
    logging.info(f"Saving readings in '{output}'")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as f:
        f.write(json.dumps(readings, indent=2))

    logging.info("Completed")
    exit(0)


if __name__ == '__main__':
    main()
