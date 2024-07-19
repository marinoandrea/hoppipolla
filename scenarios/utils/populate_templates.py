import logging
import os
import re
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass

from common import parse_ini_file


@dataclass(frozen=True)
class ProgramArguments:
    scenario: str
    debug: bool


def parse_arguments() -> ProgramArguments:
    parser = ArgumentParser(
        prog="[Hoppipolla] Scenario Generation Tool",
        description="A CLI for setting up scenarios",
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


regex_template = r"^([a-z0-9]+(?:_|-[a-z0-9]+)*)\.template\.([a-z]+)$"


def populate(scenario: str, type: str, config: ConfigParser):
    for file in os.listdir(f"{scenario}/{type}"):
        match = re.match(regex_template, file)

        if match is None:
            continue

        logging.info(f"Populating {file}")

        template_name = match.group(1)
        template_ext = match.groups()[-1]

        with open(f"{scenario}/{type}/{file}", "r") as f:
            content = f.read()

        section = f"templates.{type}.{template_name}"
        for variable in config[section]:
            value = config[section][variable]
            logging.info(f"Populating variable ${variable} with {value}")
            content = content.replace(f"${variable}", value)

        with open(f"{scenario}/{type}/{template_name}.{template_ext}", "w") as f:
            f.write(content)


def main():
    args = parse_arguments()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='[%(levelname)s]: %(message)s',
    )

    config = parse_ini_file(args.scenario)

    logging.info("Populating policy templates")
    populate(args.scenario, "policies", config)

    logging.info("Populating data templates")
    populate(args.scenario, "data", config)


if __name__ == '__main__':
    main()
