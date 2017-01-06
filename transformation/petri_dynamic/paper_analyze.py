#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tqdm
from subprocess import call


def main(f):
    print(f)
    r=0
    t = tqdm.tqdm(10)
    print("Running the transformation")
    t.update(1)
    r |= call("GrShell -N {}.grs".format(f), shell=True)
    if r != 0: return False
    t.update(1)
    print("grsi to pnml")
    r|=call("java -jar ../../tools/pnml2grgen/pnml2grgen.jar paper_flat.grsi", shell=True)
    r|=call("rm paper_flat.grsi", shell=True)
    r|=call("mv paper_flat.grsi.pnml paper_flat.pnml", shell=True)
    if r != 0: return False
    t.update(1)
    print("pnml to lola")
    r|=call("ndrio paper_flat.pnml paper_flat.lola", shell=True)
    if r != 0: return False
    t.update(1)
    print("No deadlocks:")
    r|=call('lola --path --state --formula="NOT EF DEADLOCK" paper_flat.lola', shell=True)
    if r != 0: return False
    t.update(1)
    print("Reversible:")
    r|=call('lola --path --state --formula="AGEF INITIAL" paper_flat.lola', shell=True)
    if r != 0: return False
    t.update(1)
    print("Tina")
    r|=call("tina paper_flat.pnml", shell=True)
    if r != 0: return False
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        f="paper_dfop"
    else:
        f=sys.argv[1]
    if not main(f):
        print("ERROR")
        print("ERROR")
        print("ERROR")
