from model import Node, Edge, Mgr, Element
from typing import List
import re


class GrsPrint:
    def __init__(self,
                 mgr: Mgr,
                 nodes: List[Node],
                 edges: List[Edge],
                 namespace: str=""):
        self.namespace = namespace
        self.mgr = mgr
        self.nodes = nodes
        self.edges = edges
        # internal
        self.references = {}
        self.varname_counter = 0
        self.type_prefixes = set()
        self.type_to_prefix = {}
        self.prefix_counter = {}
        self.write_references()

    def gen_varname(self, n: Node):
        self.varname_counter += 1
        prefix = self.namespace
        prefix += self.pretty_var_name(n)
        if not prefix:
            prefix = "a"
        if prefix not in self.prefix_counter:
            self.prefix_counter[prefix] = 0
        self.prefix_counter[prefix] += 1
        prefix += str(self.prefix_counter[prefix])
        return prefix

    def pretty_var_name(self, n: Node):
        if n.type in self.type_to_prefix:
            return self.type_to_prefix[n.type]
        name = n.type.name
        upper = "".join(re.findall("([A-Z])", name))
        if upper and upper.lower() not in self.type_prefixes:
            p = upper.lower()
        else:
            underscore = "".join(re.findall("_([a-z])", name))
            if underscore and underscore not in self.type_prefixes:
                p = underscore
            else:
                other = "".join(re.findall("([A-Za-z])", name)).lower()
                for i in range(2, len(other)):
                    p = other[:i]
                    if p not in self.type_prefixes:
                        break
        self.type_to_prefix[n.type] = p
        self.type_prefixes.add(p)
        return p

    def write_references(self):
        referenced = set()
        for e in self.edges:
            referenced.add(e.source)
            referenced.add(e.target)
        for n in referenced:
            self.references[n] = self.gen_varname(n)

    def print(self):
        for n in self.nodes:
            print("new ", end="")
            if n in self.references:
                print(self.references[n], end="")
            print(":" + n.type.name, end="")
            self.print_attributes(n)
            print("")
        print("# total number of nodes: %d" % len(self.nodes))
        for e in self.edges:
            print("new ", end="")
            print(self.references[e.source], end="")
            print(" -:" + e.type.name, end="")
            self.print_attributes(e)
            print("-> ", end="")
            print(self.references[e.target], end="")
            print("")
        print("# total number of edges: %d" % len(self.edges))

    def print_attributes(self, el: Element):
        print_attrs = []
        for attr in el.attributes:
            attr_definition = el.type.get_attribute(attr)
            val = el.attributes[attr]
            if el.type.get_default(attr) is not None and el.type.get_default(
                    attr) == val:
                continue
            val = attr_definition.format(el.attributes[attr])
            print_attrs.append(attr + " = " + val)

        if print_attrs:
            print("(", end="")
            print(", ".join(print_attrs), end="")
            print(")", end="")
