#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tqdm
from subprocess import call

l = [
"paper_dfop",
#"paper_dfop_conf_milk",
#"paper_dfop_conf_nomilk",
#"paper_dfop_conf_milk_dyn_1",
#"paper_dfop_conf_milk_dyn_0",
"paper_buko",
#"paper_buko_net1",
#"paper_buko_net2",
#"paper_buko_dyn_net1",
#"paper_buko_dyn_net2",
]

for i in tqdm.tqdm(l):
    cmd = "python3 paper_analyze.py {} &> {}.result".format(i,i)
    r = call(cmd,shell=True)
    print(cmd, r)
