#!/usr/bin/env python3
'''
This script parses a topology '.topo' file and generates an SVG visualization
of the network graph.
'''
import logging
import random
import sys
from argparse import ArgumentParser
from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx
from common import parse_topology_file
from matplotlib.lines import Line2D


@dataclass(frozen=True)
class ProgramArguments:
    scenario: str
    debug: bool


def parse_arguments() -> ProgramArguments:
    parser = ArgumentParser(
        prog="[Hoppipolla] scenario Visualization Tool",
        description="A CLI for generating network graph visualizations",
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


def hierarchy_pos(
    G: nx.Graph,
    root: str | None = None,
    width=1.,
    vert_gap=0.2,
    vert_loc=0.,
    xcenter=0.5
):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with
        other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError(
            'cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            # allows back compatibility with nx version 1.11
            root = next(iter(nx.topological_sort(G)))  # type: ignore
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(
        G: nx.Graph,
        root: str | None,
        width=1.,
        vert_gap=0.2,
        vert_loc=0.,
        xcenter=0.5,
        pos=None,
        parent=None
    ):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def main():
    args = parse_arguments()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='[%(levelname)s]: %(message)s',
    )

    logging.info("Parsing topology file")
    graph = parse_topology_file(f"{args.scenario}/topology.topo")

    core = nx.get_node_attributes(graph, "core")

    legend_elements = [
        Line2D([0], [0], marker='o', color='#BF616A', label='Core AS', lw=0,
               markerfacecolor='#BF616A', markersize=10),
        Line2D([0], [0], marker='o', color='#81A1C1', label='AS', lw=0,
               markerfacecolor='#81A1C1', markersize=10)]

    logging.info("Creating graph visualization")
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.legend(handles=legend_elements)
    plt.margins(0.2)
    nx.draw_networkx(
        graph,
        ax=ax,
        pos=hierarchy_pos(graph, root=next(
            node for node in graph.nodes if core[node])),
        node_size=500,
        node_color=[
            "#BF616A" if core.get(node, False) else "#81A1C1" for node in graph
        ]
    )

    output = f"{args.scenario}/assets/topology.svg"
    logging.info(f"Saving visualization in {output}")
    fig.savefig(output, bbox_inches='tight', dpi=300)

    logging.info("Completed")


if __name__ == '__main__':
    main()
