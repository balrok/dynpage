#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from subprocess import call
from dependencies import init_dependencies, find_dependencies
from modelparser import get_stats_for_models


def get_stats_for_file(filename: str) -> str:
    init_dependencies()
    files = find_dependencies(filename)
    return get_stats_for_models(files)


if __name__ == "__main__":
    grs = sys.argv[-1]
    grsi = sys.argv[1:-1]
    s = """new graph "Rules" "DefaultGraph" ;; include %s ;;""" % (
        " ;; include ".join(grsi))
    stdin = ""
    stdin += "validate\n"
    #stdin += b"%s\n" % get_stats_for_file(grs).encode("utf-8")
    print('GrShell -C \'%s\' %s' % (s, grs))
    #call(['GrShell', '-C', s, grs])
    #stdin += b"exit"
