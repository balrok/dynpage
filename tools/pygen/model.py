#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Any, List, Tuple
from enum import Enum
import re


class TypeType(Enum):
    node = 10
    a_node = 11
    directed_edge = 20
    a_directed_edge = 21
    undirected_edge = 30
    a_undirected_edge = 31
    # natural = 40 # virtual for string,int,float
    string = 41
    int = 42
    float = 43
    bool = 44

    # collection = 50 # TODO implement
    # map = 51 # TODO implement
    # set = 52 # TODO implement

    def get_type(s: str):
        s = re.sub("\s+", " ", s.strip())
        if s == "abstract node":
            return TypeType.a_node
        elif s == "node":
            return TypeType.node
        elif s == "abstract edge":
            return TypeType.a_directed_edge
        elif s == "abstract directed edge":
            return TypeType.a_directed_edge
        elif s == "edge":
            return TypeType.directed_edge
        elif s == "directed edge":
            return TypeType.directed_edge
        elif s == "abstract undirected edge":
            return TypeType.a_undirected_edge
        elif s == "undirected edge":
            return TypeType.undirected_edge
        elif s == "string":
            return TypeType.string
        elif s == "int":
            return TypeType.int
        elif s == "float":
            return TypeType.float
        elif s == "bool":
            return TypeType.bool
        raise Exception("not found " + repr(s))

    def format(self, s: Any):
        if self == self.int:
            return str(s)
        elif self == self.float:
            return str(s)
        elif self == self.bool:
            return ("false", "true")[s]
        elif self == self.string:
            return '"' + s.replace('"', '\\"') + '"'
        return s

    def parse(self, s: str):
        if self == self.int:
            return int(s)
        elif self == self.float:
            return float(s)
        elif self == self.bool:
            return bool(s)
        elif self == self.string:
            return s[1:-1].replace('\\"', '"')
        return s


class Type(object):
    """A type is a definition from the grgen model or is natural like
    int,str or is a collection"""

    def __init__(self,
                 type: TypeType,
                 name: str,
                 parents=None,
                 connections=None,
                 attributes: Dict=None,
                 defaults: Dict=None,
                 **kwargs):
        self.type = type
        self.name = name
        if not parents:
            parents = []
        self.parents = parents
        if not connections:
            connections = []
        self.connections = connections
        if not attributes:
            attributes = {}
        self.attributes = { ** attributes, ** kwargs}
        self.defaults = {}
        if defaults:
            self.defaults = defaults

    def get_attribute(self, name: str):
        if name in self.attributes:
            return self.attributes[name]
        for i in self.parents:
            a = i.get_attribute(name)
            if a: return a

    def get_default(self, name: str):
        if name in self.defaults:
            return self.defaults[name]
        for i in self.parents:
            a = i.get_default(name)
            if a is not None:
                return a


class Element(object):
    """An Element is the base for Node and Edge"""

    def __init__(self, type: Type, attributes: Dict[str, Any]=None, **kwargs):
        if not attributes:
            attributes = {}
        self.type = type
        self.attributes = { ** attributes, ** kwargs}


class Node(Element):
    """A node has attributes and can be connected to other nodes by Edge"""
    pass


class Edge(Element):
    """A node has attributes and can be connected to other nodes by Edge"""

    def __init__(self, source: Node, target: Node, **kwargs):
        self.source = source
        self.target = target
        Element.__init__(self, **kwargs)

    def set_source(self, node: Node) -> None:
        self.source = node

    def set_target(self, node: Node) -> None:
        self.target = node


class Package(object):
    """ A package contains types
    The default package is named ''
    """

    def __init__(self, name, mgr):
        self.name = name
        self.mgr = mgr
        self.types = []

    def add_type(self, type: Type) -> None:
        self.types.append(type)

    def get_type(self, name: str) -> Type:
        if not name: return None
        if ":" in name:
            return self.mgr.get_type(name)
        return self._get_type(name)

    def _get_type(self, name: str) -> Type:
        for type in self.types:
            if type.name == name:
                return type
        #print([t.name for t in self.types])
        raise Exception("Not found: " + name)


class Mgr(object):
    def __init__(self):
        default = Package("", self)
        #default.add_type(Type(TypeType.a_node, "Node"))
        self.packages = [default]

    def add_package(self, package: Package):
        self.packages.append(package)
        return package

    def get_package(self, name):
        for package in self.packages:
            if package.name == name:
                return package
        raise Exception("Not found: " + name)

    def get_create_package(self, name):
        for package in self.packages:
            if package.name == name:
                return package
        return self.add_package(Package(name, self))

    def get_packages(self) -> List[Package]:
        return self.packages

    def get_types(self) -> Tuple[Package, List[Type]]:
        for package in self.packages:
            yield (package, package.types)

    def get_type(self, name: str):
        if not name: return None
        if ":" in name:
            pname, name = name.split(":")
            package = self.get_package(pname)
        else:
            package = self.get_package("")
        return package._get_type(name)


if __name__ == "__main__":
    mgr = Mgr()
    mgr.get_create_package("")
    package = mgr.get_create_package("testpackage")
    for pkg, types in mgr.get_types():
        print(pkg, types)
