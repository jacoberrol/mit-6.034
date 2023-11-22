import os
import subprocess

import graphs
from search import Graph, Edge


def vis(graph: Graph, f: str) -> None:
    dotfile = ""
    dotfile += initvis()
    for edge in graph.edges:
        dotfile += create_edge(edge)
    for heu in graph.heuristic.keys():
        for h in graph.heuristic[heu].keys():
            dotfile += create_heuristic(graph.heuristic[heu][h], heu, h)
    dotfile += exitvis()
    with open(f"{f}.dot", "w") as f:
        f.write(dotfile)


def initvis() -> str:
    return "graph {\n"


def exitvis() -> str:
    return "}\n"


def create_edge(edge: Edge)-> str:
    return f'\t"{edge.node1}" -- "{edge.node2}" [label = "L:{edge.length}"];\n'


def create_heuristic(heuristic: int, n1: str, n2: str) -> str:
    if n1 == n2:
        return ""
    return f'\t"{n1}" -- "{n2}" [label = "H:{heuristic}", color=blue];'


if __name__ == "__main__":
    gs = [(graphs.GRAPH1, "graph1"), (graphs.GRAPH2, "graph2"), (graphs.GRAPH3, "graph3"), (graphs.GRAPH4, "graph4"), (graphs.GRAPH5, "graph5"), (graphs.AGRAPH, "agraph")]
    cdr = False
    for graph, name in gs:
        vis(graph, name)
        if cdr is False:
            os.mkdir("vis")
            cdr = True
        subprocess.run(["dot", "-Tpng", f"{name}.dot", "-o", f"vis/{name}.png"])
        os.remove(f"{os.curdir}/{name}.dot")