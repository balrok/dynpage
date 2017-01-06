from model import Mgr, TypeType


class PrettyPrinter:
    def __init__(self, mgr: Mgr, indent_string="  "):
        self.mgr = mgr
        self.indent_string = indent_string

    def indent(self, indent):
        print(self.indent_string * indent, end="")

    def prettyprint(self, indent=0):
        self.prettyprint_mgr(self.mgr, indent)

    def prettyprint_mgr(self, mgr, indent=0):
        self.prettyprint_package(mgr.get_package(""), indent)
        for package in mgr.packages:
            if package.name != "":
                self.prettyprint_package(package, indent)

    def prettyprint_package(self, pkg, indent=0):
        if pkg.name != "":
            self.indent(indent)
            print("package %s {" % pkg.name)
            indent += 1
        for type in pkg.types:
            self.prettyprint_type(type, indent)
        if pkg.name != "":
            indent -= 1
            self.indent(indent)
            print("}")

    def prettyprint_type(self, type, indent=0):
        self.indent(indent)
        self.prettyprint_typetype_definition(type.type, indent)
        print(" " + type.name, end="")
        if type.parents:
            print(
                " extends " + ", ".join([p.name for p in type.parents]),
                end="")
        if type.connections:
            indent += 1
            print("")
            self.indent(indent)
            print("connect ", end="")
            indent += 1
            c = len(type.connections)
            for source, target in type.connections:
                print(source.name + " --> " + target.name, end="")
                c -= 1
                if c > 0:
                    print(",")
                    self.indent(indent)
            indent -= 1
            indent -= 1
        if type.attributes:
            print(" {")
            indent += 1
            for attr in type.attributes:
                self.indent(indent)
                print(
                    attr + ": " +
                    self.prettyprint_typetype(type.attributes[attr]),
                    end="")
                if attr in type.defaults:
                    print(
                        " = " +
                        type.attributes[attr].format(type.defaults[attr]),
                        end="")
                print(";")
            indent -= 1
            self.indent(indent)
            print("}")
        else:
            self.indent(indent)
            print(";")
            print("")

    def prettyprint_typetype_definition(self, typetype, indent=0):
        if typetype == TypeType.node: print("node class", end="")
        if typetype == TypeType.a_node: print("abstract node class", end="")
        if typetype == TypeType.directed_edge: print("edge class", end="")
        if typetype == TypeType.undirected_edge:
            print("undirected edge class", end="")
        if typetype == TypeType.a_directed_edge:
            print("abstract edge class", end="")
        if typetype == TypeType.a_undirected_edge:
            print("abstract undirected edge class", end="")

    def prettyprint_typetype(self, typetype, indent=0):
        if typetype == TypeType.string: return "string"
        elif typetype == TypeType.int: return "int"
        elif typetype == TypeType.float: return "float"
        elif typetype == TypeType.bool: return "bool"
        else: return "unknown_type"
