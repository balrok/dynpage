#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

grsi_id = 0


def fix_grsi_file(new_graph: str) -> None:
    """
        Will remove the "new graph" statement from a grsi file
        And give a unique id
    """
    global grsi_id
    grsi_id += 1

    with open(new_graph, "r+") as f:
        content = f.readlines()
        f.seek(0)
        for line in content:
            if line.startswith("new graph "):
                line = "# " + line
            line = re.sub(r'\$ = "\$([a-zA-Z0-9_]+)"', r'$ = "$%s_\1"' %
                          grsi_id, line)
            line = re.sub(r'@\("\$([a-zA-Z0-9_]+)"\)', r'@("$%s_\1")' %
                          grsi_id, line)
            # assignment to variables
            # there was a grgen bug - fix in 4.4.6
            # line = re.sub(r'(\.[a-zA-Z0-9_]+ = )"\$([a-zA-Z0-9_]+)"', r'\1 @("$%s_\2")' % grsi_id, line)
            # keyword inside constructor
            line = line.replace(', num = ', ', "num" = ')
            f.write(line)
        f.truncate()


if __name__ == "__main__":
    import sys
    fix_grsi_file(sys.argv[1])
