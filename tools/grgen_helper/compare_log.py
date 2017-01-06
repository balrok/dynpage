import difflib


def compare(logA, logB):
    are_different = False
    for line in difflib.ndiff(logA, logB):
        if line.startswith("- ") or line.startswith("+ "):
            if line[2:].startswith(
                    "Executing Graph Rewrite Sequence done after") or line[
                        2:].startswith("Searchplans for actions"):
                continue
            # Graph 'DefaultGraph' analyzed in 1 ms.
            if line[2:].startswith("Graph '") and line.endswith(" ms."):
                continue
            if line[2:].startswith("Building libraries..."):
                continue
            if line[2:].startswith("export done after"):
                continue
            if line[2:].startswith(" - Model assembly \""):
                continue
            if line[2:].startswith(" - Actions assembly \""):
                continue
            print(line)
            are_different = True
    return are_different
