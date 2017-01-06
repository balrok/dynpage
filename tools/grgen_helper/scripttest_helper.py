import os
import shutil
from typing import List
import subprocess
import sys
#import asyncio

from .lib.scripttest import ProcResult, TestFileEnvironment, clean_environ, string
from . import get_stats_for_file


def copy_env_results(r: ProcResult, out: str) -> None:
    if out is None:
        return

    if not os.path.exists(out):
        os.makedirs(out)

    print(20 * "-")
    print(out)
    for f in r.files_created:
        full = r.files_created[f].full
        shutil.copyfile(full, os.path.join(out, f))
    for f in r.files_updated:
        full = r.files_updated[f].full
        shutil.copyfile(full, os.path.join(out, f))


def run_shell(env: TestFileEnvironment, file: str,
              artifacts: List[str]) -> (ProcResult, str):
    args = file.split(" ")
    cmd = args[0]
    del (args[0])
    args += artifacts
    r = env.run(cmd, expect_error=True, *args)
    printable_args = [i if i.startswith("-") else "'" + i + "'" for i in args]
    cmd = cmd + " " + " ".join(printable_args)
    return r, cmd


#grs_cache = {}
#def start_grs(grshell_bin: str, folder:str):
#    args = []
#    args.append("-N")
#    all = [grshell_bin] + args
#    proc = asyncio.create_subprocess_exec(all,
#                            stdin=asyncio.PIPE,
#                            stderr=asyncio.PIPE,
#                            stdout=asyncio.PIPE,
#                            cwd=folder,
#                            # see http://bugs.python.org/issue8557
#                            shell=(sys.platform == 'win32')
#                            )
#
#
#    proc = subprocess.Popen(all,
#                            stdin=subprocess.PIPE,
#                            stderr=subprocess.PIPE,
#                            stdout=subprocess.PIPE,
#                            cwd=folder,
#                            # see http://bugs.python.org/issue8557
#                            shell=(sys.platform == 'win32')
#                            )
#    grs_cache[folder] = proc


def run_chain_script_grs(grshell_bin: str,
                         env: TestFileEnvironment,
                         file: str,
                         new_graph: str=None,
                         last_graphs: List[str]=None,
                         validate: bool=False) -> (ProcResult, str):

    args = []
    args.append("-N")
    if last_graphs is not None and len(last_graphs) > 0:
        args.append("-C")
        #s="cd %s;; include %s;; cd %s" % (os.path.dirname(last_graph), os.path.basename(last_graph), env.cwd)
        s = """new graph "Rules" "DefaultGraph" ;; include %s ;;\n\n""" % (
            " ;; include ".join(last_graphs))
        args.append(s)
    args.append(file)

    stdin = b""
    if len(new_graph) > 0 and new_graph[0].endswith(".grsi"):
        stdin += b"export %s\n" % new_graph[0].encode("utf-8")
    if validate:
        stdin += b"validate\n"
    stdin += b"%s\n" % get_stats_for_file(
        os.path.join(env.base_path, file), env.base_path).encode("utf-8")

    #r = env.run(grshell_bin, stdin=stdin, expect_error=True, *args)
    all = [grshell_bin] + args
    #if env.base_path in grs_cache:
    #    proc = grs_cache[env.base_path]
    #    stdin = stdin_first + stdin
    #else:
    proc = subprocess.Popen(
        all,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        cwd=env.base_path,
        # see http://bugs.python.org/issue8557
        shell=(sys.platform == 'win32'),
        env=clean_environ(env.environ))
    stdin += b"exit"
    #print(stdin)
    stdout, stderr = proc.communicate(stdin)
    #proc.stdin.write(stdin)
    #stdout = proc.stdout.read()
    #stderr = proc.stderr.read()

    stdout = string(stdout)
    stderr = string(stderr)
    r = ProcResult(
        env,
        all,
        stdin,
        stdout,
        stderr,
        returncode=proc.returncode,
        files_before={},
        files_after={})

    printable_args = [i if i.startswith("-") else "'" + i + "'" for i in args]
    cmd = grshell_bin + " " + " ".join(printable_args)
    #cmd += str(args)+str(last_graphs)
    return r, cmd


def hasError(r: ProcResult) -> bool:
    return len(r.stderr) > 0 or r.returncode != 0
