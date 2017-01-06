#!/usr/bin/env python3

import os
import time
from typing import List
import sys
from shutil import copyfile

from grgen_helper.lib.scripttest import TestFileEnvironment
from grgen_helper.log import log, indent, unindent, indent_reset, loge
from grgen_helper.fix_grsi_file import fix_grsi_file
from grgen_helper.scripttest_helper import copy_env_results, run_shell, run_chain_script_grs, hasError
#from grgen_helper.scripttest_helper import start_grs
from .lib import tqdm

grshell_bin = 'GrShell'

last_graphs = []

#last_graph = os.path.abspath("petri2circuit/chain_circle.grsi")

# chainideas:
# * large contextmodel
#   -> transformed into vhdl
# * combined workflow
#   - contextmodel specification
#   - Petri net specification - placeholder for context-places
#   - transform both in petri net
#   - combine
#   - into vhdl
#
# TODO
#   * run other command types
#       * executy .py
#       * execute .vhdl
#   * specify input
#       not just at the beginning e.g. input for contexts, pnml file, later some vhdl spec / platform spec
#   * specify export/import requirements:
#       * e.g. two PetriNet pages need to be merged - so the previous chain steps need to export it
#       * and the next chain step needs to import it
#   * commandline options / dsl for chain specification
#   * visualize everything - best would be to generate 1 .grs file which then does debug exec everything - but not possible because of rules/model?


class Command(object):
    def __init__(self,
                 folder: str="",
                 file: str="",
                 artifacts: List[str]=None,
                 expect_error: bool=False,
                 params=None,
                 descr: str=None,
                 add_artifacts: List[str]=None):
        self.folder = os.path.abspath(folder)
        self.file = file
        self.set_artifacts(artifacts)
        self.children = []
        self.next = []
        self.expect_error = expect_error
        if params is None:
            params = ["%s0", "%s1", "%s2"]
        self.params = params
        self.output_dir = None
        if descr is not None:
            self.descr = descr
        else:
            self.descr = folder
        if add_artifacts is None:
            self.add_artifacts = []
        else:
            self.add_artifacts = add_artifacts

    def set_artifacts(self, artifacts):
        if isinstance(artifacts, str):
            artifacts = [artifacts]
        if not artifacts and self.file.endswith(".grs"):
            artifacts = [self.file + ".grsi"]
        if not artifacts:
            artifacts = []
        self.artifacts = [(x, os.path.join(self.folder, x))["%s" not in x]
                          for x in artifacts]

    def addChild(self, cmd):
        """ add more commands under the same parent results """
        self.children.append(cmd)
        return self

    def addNext(self, cmd):
        self.next.append(cmd)
        return self

    def getParamsList(self, params: List[str],
                      artifacts: List[str]) -> List[str]:
        ret = params[:]
        for i in range(0, 3):
            if i < len(artifacts):
                s = artifacts[i]
            else:
                s = ""
            ret = [x.replace("%s" + str(i), s) for x in ret]
        ret = [x for x in ret if x.strip() != ""]
        return ret

    def getParamsString(self, params: str, artifacts: List[str]) -> str:
        ret = params[:]
        for i in range(0, 3):
            if i < len(artifacts):
                s = artifacts[i]
            else:
                s = ""
            ret = ret.replace("%s" + str(i), s)
        return ret.strip()

    def execute(self, artifacts: List[str]) -> List[str]:
        if self.file == "":
            gen_report(self.folder, "", "", 0, self.descr)
            return []
        log("Chain step: %s %s" % (self.folder, self.file))
        indent()
        # TODO execute the specified script
        env = TestFileEnvironment(self.folder, start_clear=False)
        start_time = time.time()
        my_artifacts = artifacts + self.add_artifacts
        try:
            os.makedirs(self.output_dir)
        except:
            pass
        if self.file.endswith(".grs"):
            r, cmd = run_chain_script_grs(grshell_bin, env,
                                          self.getParamsString(self.file,
                                                               my_artifacts),
                                          self.artifacts, my_artifacts)
        else:
            r, cmd = run_shell(env,
                               self.getParamsString(self.file, my_artifacts),
                               self.getParamsList(self.params, my_artifacts))
            copy_env_results(r, self.output_dir)

        if not hasError(r) or self.expect_error:
            if len(self.artifacts) > 0 and self.artifacts[0].endswith(".grsi"):
                fix_grsi_file(self.artifacts[0])
        duration = time.time() - start_time

        result = r.__str__()
        gen_report(self.folder, result, cmd, duration, self.descr)
        log(cmd)
        if self.file.endswith(".grs"):  # why only .grs?
            print(self.artifacts)
        if hasError(r):
            loge("Error in execution")
            if not self.expect_error:
                loge("stopping because of an error")
                print_reports()
                loge(r.stdout)
                loge(r.stderr)
                sys.exit(1)

        ret = [
            self.getParamsString(artifact, my_artifacts)
            for artifact in self.artifacts
        ]
        for artifact in ret:
            print("cp %s %s" % (artifact,
                     os.path.join(self.output_dir, os.path.basename(artifact))))
            copyfile(artifact,
                     os.path.join(self.output_dir, os.path.basename(artifact)))
        log("Finished execution - returned following artifacts: %s" % ret)
        return ret

    def run_children(self, artifact: List[str]) -> List[str]:
        ret = []
        indent()
        for cmd in self.children:
            ret += cmd.run(artifact)
        unindent()
        return ret

    def run_next(self, artifacts: List[str]) -> List[str]:
        ret = []
        for cmd in self.next:
            ret += cmd.run(artifacts)
        return ret

    def run(self, artifacts: List[str]=None) -> List[str]:
        self.pbar.update(1)
        #tqdm.tqdm.write(self.folder)
        if artifacts is None:
            artifacts = []
        result = self.execute(artifacts)
        artifacts = self.run_children(result)
        log("after children")
        log(str(artifacts))
        self.run_next(artifacts)
        if len(artifacts) == 0:
            artifacts = self.artifacts
        log("RETURN")
        log(str(artifacts))
        return artifacts

    def __str__(self, indent=0):
        ret = ["%s%s" % (indent * "  ", self.folder)]
        for cmd in self.children:
            ret.append(cmd.__str__(indent + 1))
        for cmd in self.next:
            ret.append(cmd.__str__(indent))
        return "\n".join(ret)


chain = Command("context2petri", "chain.grs")

report_list = []  # type: List[dict]
global_start_time = time.time()


def gen_report(dir: str, res: str, cmd: str, duration: float,
               description: str) -> None:
    stats = []  # type List[str]
    for i in res.splitlines():
        if i.replace("> ",
                     "").startswith("Number of") and not i.endswith(" 0"):
            stats.append(i.replace("> ", ""))
        elif i.startswith(" - ") and i.endswith("matches found"):
            stats.append(i)
        elif i.startswith(" - ") and i.endswith("rewrites performed"):
            stats.append(i)

    report_list.append({
        "dir": dir,
        "commands": [
            "cd {};".format(dir),
            "{}".format(cmd),
        ],
        "stats": stats,
        "duration": duration,
        "description": description,
    })


def print_reports(output_dir: str=None):
    sum_duration = sum([r["duration"] for r in report_list])
    import re
    stats = []

    for report in report_list:
        print(report["dir"])
        print("-" * 20)
        for cmd in report["commands"]:
            print("    %s" % cmd)
        print("     duration: %03f (%d%%)" %
              (report["duration"], report["duration"] / sum_duration * 100))
        print("     stats:")
        s = []
        for stat in report["stats"]:
            print("    %s" % stat)
            res = re.match(
                '.*(node|edge)s compatible to type "([a-zA-Z]+)": ([0-9]+)',
                stat)
            if res:
                s.append(
                    re.match(
                        '.*(node|edge)s compatible to type "([a-zA-Z]+)": ([0-9]+)',
                        stat).groups())
        stats.append(s)
    if output_dir:
        import csv
        dict_stats = []
        all_keys = []
        for i, s in enumerate(stats):
            d = {}
            for item in s:
                d[item[0] + "_" + item[1]] = item[2]
            d["step"] = report_list[i]["description"]
            dict_stats.append(d)
            all_keys += list(d.keys())
        all_keys = list(set(all_keys))
        all_keys.sort(reverse=True)
        with open(os.path.join(output_dir, 'chain.csv'), 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=all_keys,
                quotechar='"',
                delimiter=';',
                quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for d in dict_stats:
                writer.writerow(d)

    print("Sum duration: %02f" % sum([r["duration"] for r in report_list]))
    print("Real duration: %02f" % (time.time() - global_start_time))


def iterate_all_commands(c: Command):
    yield (c)
    for cc in c.children:
        for r in iterate_all_commands(cc):
            yield r
    for cn in c.next:
        for r in iterate_all_commands(cn):
            yield r


def run(chain: Command, output_dir: str) -> None:
    common_prefix = len(
        os.path.dirname(
            os.path.commonprefix(
                [c.folder for c in iterate_all_commands(chain)]))) + 1
    number_of_commands = 0
    for c in iterate_all_commands(chain):
        c.output_dir = os.path.join(output_dir, c.folder[common_prefix:])
        number_of_commands += 1
        #start_grs(grshell_bin, c.folder)

    indent_reset()
    print(chain)
    with tqdm.tqdm(total=number_of_commands) as pbar:
        for c in iterate_all_commands(chain):
            c.pbar = pbar
        chain.run()

    log("These scripts were executed")
    print_reports(output_dir)


if __name__ == "__main__":
    run(chain)
