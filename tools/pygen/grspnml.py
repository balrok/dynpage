#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import snakes.nets
import snakes.pnml
import sys
from typing import List, Dict
from model import Mgr
from pygen import parse_model, parse_grsi
import os
import functools


def help():
    print("Convert GrGen.net GRS-files to PNML or the other way round")
    print("Only works for my Meta-Model")
    print("Arguments:")
    print(" - Petri net model(s) in GrGen.net format (.gm)")
    print(" either:")
    print("   - File ending with grs")
    print("   - File ending with pnml")
    print(" - directory or file which will be used for output")


def main(gm: List[str], source: str, output: str) -> None:
    for g in gm:
        if not os.path.exists(g):
            print("Does not exist: " + g)
            sys.exit(1)
    if not os.path.exists(source):
        print("Does not exist: " + source)
        sys.exit(1)
    print("Loading source: %s" % source)
    print("Depending on gm-files: %s" % ", ".join(gm))
    mgr = Mgr()
    for g in gm:
        parse_model(open(g).read(), mgr)
    if source.endswith(".grs") or source.endswith(".grsi"):
        convert_from_grs(mgr, source, output)
    elif source.endswith(".pnml"):
        convert_from_pnml(mgr, source, output)


def build_mapping(mgr: Mgr) -> Dict:
    mapping = {}
    for pkg, types in mgr.get_types():
        for type in types:
            # snakes has no pages -> merge all nodes of a page into a PetriNet
            if type.name == "Page":
                mapping[type] = snakes.nets.PetriNet
            elif type.name == "Place":
                mapping[type] = functools.partial(
                    snakes.nets.Place, check=snakes.nets.tBlackToken)
            elif type.name == "Transition":
                mapping[type] = snakes.nets.Transition
            elif type.name == "Token":
                mapping[type] = snakes.nets.BlackToken
                #snakes.nets.BlackToken
                #snakes.nets.Inhibitor
    return mapping


def convert_from_grs(mgr: Mgr, source: str, output: str):
    nodes, edges = parse_grsi(open(source).read(), mgr)
    mapping = build_mapping(mgr)
    node_map = {}
    for n in nodes:
        if n.type in mapping:
            if "id" in n.attributes:
                node_map[n] = mapping[n.type](n.attributes["id"])
            else:
                node_map[n] = mapping[n.type]()
        else:
            print("unhandled node ", n.type.name)
    for e in edges:
        if e.type.name == "places":
            node_map[e.source].add_place(node_map[e.target])
        elif e.type.name == "transitions":
            node_map[e.source].add_place(node_map[e.target])
        elif e.type.name == "tokens":
            node_map[e.source].add(snakes.nets.dot)
        elif e.type.name == "inArc":
            node_map[e.source].add_input(node_map[e.target],
                                         snakes.nets.Value(1))
        elif e.type.name == "outArc":
            node_map[e.target].add_output(node_map[e.source],
                                          snakes.nets.Value(1))
        else:
            print("unhandled edge ", e.type.name)

    for n in node_map:
        if isinstance(node_map[n], snakes.nets.PetriNet):
            pn = node_map[n]
            open(os.path.join(output, pn.name + ".pnml"),
                 "w").write(snakes.pnml.dumps(pn))


def convert_from_pnml(mgr: Mgr, source: str, output: str):
    pn = snakes.pnml.loads(open(source).read())
    print(pn, output)


if __name__ == "__main__":
    gm = []
    for i in sys.argv[1:-1]:
        if i.endswith(".gm"):
            gm.append(i)
    source = None
    for i in sys.argv[1:-1]:
        if i.endswith(".grsi") or i.endswith(".grs") or i.endswith(".pnml"):
            source = i
            break

    output = sys.argv[-1]
    if output.endswith(".pnml"):
        raise Exception("TODO .pnml")

    if len(sys.argv) < 3:
        help()
        sys.exit(1)
    main(gm, source, "out")
