from typing import List, Tuple
import re

re_name = "(?P<name>[a-zA-Z0-9_]+)"
re_extends = "(\s+extends\s+(?P<parent>[a-zA-Z0-9_]+\s*,?\s*)+)?"


class Model(object):
    def __init__(self,
                 name: str,
                 parent: str=None,
                 attributes: List[str]=[],
                 package: str=""):
        self.name = name
        self.parent = parent
        self.attributes = attributes
        self.parent_model = None
        self.package = package

    def getIdentifier(self):
        if self.package != "":
            return self.package + "::" + self.name
        return self.name


class Node(Model):
    def __init__(self,
                 name: str,
                 parent: str=None,
                 attributes: List[str]=[],
                 package: str=""):
        super().__init__(name, parent, attributes, package)


class Edge(Model):
    def __init__(self,
                 name: str,
                 type: str,
                 parent: str=None,
                 attributes: List[str]=[],
                 package: str=""):
        super().__init__(name, parent, attributes, package)
        self.type = name


def parse_model(filename: str) -> Tuple[List[Node], List[Edge]]:
    node_list = []
    edge_list = []
    package = ""
    if filename.endswith(".gm"):
        content = ""
        with open(filename) as f:
            content = f.readlines()
        for line in content:
            # package test {
            m = re.search("^\s*package " + re_name + "\s*(\{)\s*$", line)
            if m:
                package = m.group("name")
            # node class Transition extends TransitionNode;
            m = re.search("^\s*node class " + re_name + re_extends +
                          "\s*(;|\{)\s*$", line)
            if m:
                node_list.append(
                    Node(
                        m.group("name"), m.group("parent"), package=package))
                continue
            #abstract directed edge class Arc extends EIdent;
            m = re.search("^\s*((?P<type>[a-zA-Z0-9 ]+)\s+)?edge class " +
                          re_name + re_extends + "\s*(;|\{)?\s*$", line)
            if m:
                edge_list.append(
                    Edge(
                        m.group("name"),
                        m.group("type"),
                        m.group("parent"),
                        package=package))
                continue
    return node_list, edge_list


def parse_models(filenames: List[str]) -> Tuple[List[Node], List[Edge]]:
    all_nodes = []
    all_edges = []
    for filename in filenames:
        node_list, edge_list = parse_model(filename)
        all_nodes = all_nodes + node_list
        all_edges = all_edges + edge_list
    find_parent_model(all_nodes)
    find_parent_model(all_edges)
    return all_nodes, all_edges


def find_parent_model(models: List[Model]):
    def find_by_name(name: str):
        for i in models:
            if i.name == name:
                return i

    for i in models:
        if i.parent:
            m = find_by_name(i.parent)
            i.parent_model = m


def stats_queries(type: str, models: List[Model]) -> str:
    ret = []
    ret.append("show num {}".format(type))
    for i in models:
        ret.append("show num {} {}".format(type, i.getIdentifier()))
    return "\n".join(ret)


def get_stats_for_models(filenames: List[str]) -> str:
    n, e = parse_models(filenames)
    ret = []
    ret.append(stats_queries("nodes", n))
    ret.append(stats_queries("edges", e))
    return "\n".join(ret)
