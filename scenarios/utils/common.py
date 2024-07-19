import logging
import os
import re
from configparser import ConfigParser
from enum import Enum

import networkx as nx

regex_as = r"\"([0-9]+-([0-9a-fA-F]{1,4}:){2}[0-9a-fA-F]{1,4})\":"
regex_as_attribute = r"([a-z0-9]+(?:_[a-z0-9]+)*):\s*(.+)"
regex_edge_as = r"\"([0-9]+-([0-9a-fA-F]{1,4}:){2}[0-9a-fA-F]{1,4})#([0-9]+)\""
regex_edge = r"-\s\{a:\s*" + regex_edge_as + r"\s*,\s*b:\s*" + regex_edge_as


class ParserState(Enum):
    START = 0
    PARSING_ASES = 1
    PARSING_EDGES = 2
    END = 3


def parse_topology_file(
    path: str,
    logger=logging.getLogger()
) -> nx.Graph:
    if not os.path.exists(path):
        raise ValueError(f"Topology file '{path}' was not found")

    graph = nx.Graph()
    current_isd_as = None

    with open(path, "r") as f:
        state = ParserState.START

        for line in f.readlines():
            logger.debug(f"[{state}] Parsing line {line[:-1]}")

            if state == ParserState.END:
                break

            stripped = line.strip()

            if state == ParserState.START and line.startswith("ASes"):
                state = ParserState.PARSING_ASES
                continue

            if state == ParserState.PARSING_ASES and line.startswith("links"):
                state = ParserState.PARSING_EDGES
                continue

            if state == ParserState.PARSING_ASES:
                match = re.match(regex_as, stripped)
                if match is None:
                    match = re.match(regex_as_attribute, stripped)
                    if match is None:
                        raise ValueError(f"{line} has unknown format")
                    name = match.group(1)
                    value = match.group(2)
                    if "true" in value or "false" in value:
                        graph.nodes[current_isd_as][name] = bool(value)
                        continue
                    graph.nodes[current_isd_as][name] = value
                    continue
                current_isd_as = match.group(1)
                graph.add_node(current_isd_as)
                continue

            if state == ParserState.PARSING_EDGES:
                match = re.match(regex_edge, stripped)
                if match is None:
                    state = ParserState.END
                    continue
                as_a = match.group(1)
                as_a_if = match.group(3)
                as_b = match.group(4)
                as_b_if = match.group(6)
                graph.add_edge(as_a, as_b)
                graph.edges[as_a, as_b]["if_a"] = as_a_if
                graph.edges[as_a, as_b]["if_b"] = as_b_if
                continue

    return graph


def parse_ini_file(scenario: str) -> ConfigParser:
    parser = ConfigParser()
    # see https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    setattr(parser, "optionxform", str)
    parser.read(f"{scenario}/hoppipolla.ini")
    return parser
