#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model import TypeType, Type, Mgr, Node, Edge
from pretty import PrettyPrinter
from typing import List, Tuple
from grsprint import GrsPrint

# parsing of models and grsi is simple and we do it in python

import re

re_name = "(?P<name>[a-zA-Z0-9_]+)"
re_var1 = re_name.replace("name", "var1")
re_id = "@\s*\(\s*\"(?P<id>[^\"]+)\s*\"\s*\)"
re_id1 = re_id.replace("id", "id1")
re_var2 = re_name.replace("name", "var2")
re_id2 = re_id.replace("id", "id2")
re_var3 = re_name.replace("name", "var3")
re_id3 = re_id.replace("id", "id3")
re_type = "(?P<type>[a-zA-Z0-9_]+)"
re_extends = "(\s+extends\s+(?P<parent>[a-zA-Z0-9_]+\s*,?\s*)+)?"


def parse_model(content: str, mgr: Mgr) -> Mgr:
    content = content.split("\n")
    # context is a list with the latest contexts
    # a context can be Type for example - when it finds attribute-declarations the are added to the last context
    context = []
    # package is the current active package
    # will start with the default one
    # is probably not needed if the context-array was correctly used
    # package = mgr.get_create_package("")
    context.append(mgr.get_create_package(""))
    # a flag to know when to parse attributes - probably not needed when we correctly use the contexts
    parse_attributes = False
    for line in content:
        line = re.sub("\/\/.*", "", line.strip())
        # package test {
        if len(context) == 1:
            m = re.search("^\s*package " + re_name + "\s*(\{)\s*$", line)
            if m:
                package = mgr.get_create_package(m.group("name"))
                context.append(package)
                continue
        if len(context) <= 2:
            m = re.search("^\s*((?P<type>(abstract +)?[a-zA-Z0-9 ]+))\s+class "
                          + re_name + re_extends + "\s*(;|\{)?\s*$", line)
            if m:
                package = context[-1]
                tt = TypeType.get_type(m.group("type"))
                parents = None
                if m.group("parent"):
                    parents = [
                        package.get_type(p.strip())
                        for p in m.group("parent").split(",")
                    ]
                type = Type(tt, m.group("name"), parents=parents)
                package.add_type(type)
                if "{" in line or ";" not in line:
                    context.append(type)
                    parse_attributes = True
                continue
        if "{" in line and isinstance(context[-1], Type):
            parse_attributes = True
        if "}" in line and isinstance(context[-1], Type):
            parse_attributes = False
        if "-->" in line:
            print(context)
            package = context[-2]
            line2 = re.sub(r"(\[.\]|\[\d+:\d+\]|connect\s|,|;)", "", line)
            source, target = line2.split("-->")
            source = package.get_type(source.strip())
            target = package.get_type(target.strip("{").strip())
            context[-1].connections.append((source, target))
            if ";" in line:
                del context[-1]
            continue
        if parse_attributes:
            m = re.search("^\s*" + re_name + "\s*:\s*" + re_type +
                          "\s*(=\s*(?P<value>.*?)\s*)?;\s*$", line)
            if m:
                context[-1].attributes[m.group("name")] = TypeType.get_type(
                    m.group("type"))
                if m.group("value"):
                    context[-1].defaults[m.group("name")] = TypeType.get_type(
                        m.group("type")).parse(m.group("value"))
                continue
        if "/*" in line:
            context.append("comment")
        if "*/" in line and context[-1] == "comment":
            del context[-1]
            continue
        if context[-1] == "comment":
            continue
        if "{" in line:
            context.append("unknown")
        if "}" in line:
            del context[-1]
            continue
        if line.strip() not in "}":
            print("ERROR: " + line)
    return mgr


re_attrs = "(?P<attrkey>.+?)\s*=\s*(?P<attrval>.*?)\s*(,|$)\s*"


def parse_grsi(content: str, mgr: Mgr) -> Tuple[List[Node], List[Edge]]:
    content = content.split("\n")
    nodes = []
    edges = []
    by_name = {}
    by_id = {}
    for line in content:
        line = line.strip()
        line = re.sub("\/\/.*", "", line)
        if line.startswith("new "):
            m = re.search("^new\s+" + re_name + "?\s*:\s*" + re_type +
                          "\s*(\(\s*(?P<attributes>.*)\s*\))?\s*$", line)
            if m:
                t = mgr.get_type(m.group("type"))
                idattr = None
                attrs = {}
                if m.group("attributes"):
                    a = re.findall(re_attrs, m.group("attributes"))
                    for i in a:
                        attr_type = t.get_attribute(i[0])
                        if attr_type:
                            attrs[i[0]] = attr_type.parse(i[1])
                        elif i[0] == "$":
                            idattr = i[1]
                        else:
                            print(t.name)
                            print("Attr not found: " + repr(i))
                n = Node(t, attrs)
                if m.group("name"):
                    by_name[m.group("name")] = n
                if idattr:
                    by_id[idattr[1:-1]] = n
                nodes.append(n)
                continue
            m = re.search("^new\s+(" + re_var1 + "|" + re_id1 + ")\s*" + "-\s*"
                          + re_var2 + "?\s*:\s*" + re_type +
                          "\s*(\(\s*(?P<attributes>.*)\s*\))?\s*->\s*" + "(" +
                          re_var3 + "|" + re_id3 + ")\s*$", line)
            if m:
                t = mgr.get_type(m.group("type"))
                idattr = None
                attrs = {}
                if m.group("attributes"):
                    a = re.findall(re_attrs, m.group("attributes"))
                    for i in a:
                        attr_type = t.get_attribute(i[0])
                        if attr_type:
                            attrs[i[0]] = attr_type.parse(i[1])
                        elif i[0] == "$":
                            idattr = i[1]
                        else:
                            print(t.name)
                            print("Attr not found: " + repr(i))
                if m.group("var1"):
                    source = by_name[m.group("var1")]
                else:
                    source = by_id[m.group("id1")]

                if m.group("var3"):
                    target = by_name[m.group("var3")]
                else:
                    target = by_id[m.group("id3")]

                e = Edge(
                    source=source, target=target, type=t, attributes=attrs)
                if m.group("var2"):
                    by_name[m.group("var2")] = e
                if idattr:
                    by_id[idattr] = e
                edges.append(e)
            else:
                print("ERROR", line)
    return nodes, edges


#new pn:PetriNet(id="Petri Net")
#new pn -:pages-> net

if __name__ == "__main__":
    import sys
    mgr = Mgr()
    nodes = []
    for i in sys.argv[1:]:
        with open(i) as f:
            content = f.read()
            if i.endswith(".gm"):
                parse_model(content, mgr)
            if i.endswith(".grsi") or i.endswith(".grs"):
                nodes += parse_grsi(content, mgr)
    p = PrettyPrinter(mgr, "  ")
    print("-" * 100)
    print("Prettyprint Model:")
    print("-" * 100)
    p.prettyprint()
    if nodes:
        g = GrsPrint(mgr, *nodes)
        print("-" * 100)
        print("Prettyprint Instance:")
        print("-" * 100)
        g.print()
