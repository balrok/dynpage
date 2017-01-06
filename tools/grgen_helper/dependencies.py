# a super simple grgen parser to find dependencies
import re
import os
from typing import List

dependencies = None  # type: List[str]
filesearch = "[a-zA-Z0-9._/]"  # type: str


def init_dependencies() -> None:
    global dependencies
    dependencies = []


def find_dependencies(filename: str, folder: str=None) -> List[str]:
    new_dependencies = []  # type: List[str]
    dependencies.append(filename)
    content = ""
    if folder is None:
        folder = os.path.dirname(filename)
    with open(filename) as f:
        content = f.readlines()
    if filename.endswith(".grs") or filename.endswith(".grsi"):
        new_dependencies = find_dependencies_grs(filename, folder, content)
    if filename.endswith(".grg"):
        new_dependencies = find_dependencies_grg(filename, content)
    if filename.endswith(".gm"):
        new_dependencies = find_dependencies_gm(filename, content)
    for i in new_dependencies:
        if i not in dependencies:
            find_dependencies(i)
    return dependencies


def find_dependencies_grs(filename: str, dir: str,
                          content: List[str]) -> List[str]:
    found = []  # type: List[str]
    for line in content:
        m = re.search("^\s*new\s+graph\s+\"?(" + filesearch + "+)\"?(\s|$)",
                      line)
        if m:
            f = m.group(1)
            if not f.endswith(".grg"):
                f += ".grg"
            found.append(os.path.abspath(os.path.join(dir, f)))
            continue
        m = re.search("^\s*include\s+\"?(" + filesearch + "+)\"?(\s|$)", line)
        if m:
            f = m.group(1)
            found.append(os.path.abspath(os.path.join(dir, f)))
    return found


# new graph "Rules.grg"
# new graph "Rules"
# new graph "Rules" "DefaultGraph"
# include ../petri/pn.layout
# include dyn.layout


def find_dependencies_grg(filename: str, content: List[str]) -> List[str]:
    found = []  # type: List[str]
    dir = os.path.dirname(filename)
    for line in content:
        m = re.search("^\s*#using\s+\"?(" + filesearch + "+)\"?(\s|$)", line)
        if m:
            f = m.group(1)
            found.append(os.path.abspath(os.path.join(dir, f)))
            continue
        m = re.search("^\s*#include\s+\"?(" + filesearch + "+)\"?(\s|$)", line)
        if m:
            f = m.group(1)
            found.append(os.path.abspath(os.path.join(dir, f)))
            continue
    return found


# #using "../petri/PetriModel.gm"
# #using "Model.gm"
# #include "../petri/Rules.grg"


def find_dependencies_gm(filename: str, content: List[str]) -> List[str]:
    return []


#init_dependencies()
##res = find_dependencies("/Users/cmai/Desktop/reconfnet/grgen/contextnet/petri/test.grs")
##res = find_dependencies("/Users/cmai/Desktop/reconfnet/grgen/contextnet/context2petri/chain.grs")
#res = find_dependencies("/Users/cmai/Desktop/reconfnet/grgen/contextnet/petri_dynamic/test.grs")
#for i in res:
#    print(i)
if __name__ == "__main__":
    init_dependencies()
    import sys
    files = find_dependencies(sys.argv[1])
    import pprint
    from modelparser import get_stats_for_models
    pprint.pprint(get_stats_for_models(files))
