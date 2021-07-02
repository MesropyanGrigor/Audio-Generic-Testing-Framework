"""Generic testing framework

Wraper for pytest tool
"""
import argparse
import sys
import shlex
import subprocess

import settings as setting

class LoadSettings:
    pass


class RunTests:
    """
    A class wraper into pytest tool for running tests

    Parameters
    ----------
    pytest_options : list
        pytest options to pass into pytest tool
    log : str
        log file name to keep the pytest output into that file
    """
    def __init__(self, pytest_options, log=None):
        self.cmd = f"python -m pytest {' '.join(pytest_options)}"
        self.log=log

    def run(self):
        print(f"Running pytest command: {self.cmd}")
        if self.log is not None:
            with open(self.log, 'w') as log_file:
                popen = subprocess.Popen(shlex.split(self.cmd),
                                        stdout=log_file, stderr=log_file)
                p_wait = popen.wait()
            return p_wait
        else:
            popen = subprocess.Popen(shlex.split(self.cmd))
            return popen.wait()


def parse_args(argv):
    """Argument Parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', dest='config',
                        help="Config file path")
    parser.add_argument('-np', dest='np', type=int,
                        help=("Running in parallel mode, "
                              "using provided value as number of cores"))
    parser.add_argument('-l', dest='list_tests', action="store_true", 
                        help="Show available tests")
    parser.add_argument('-log', dest='log', 
                        help="Keep pytest output into log file")
    parser.add_argument('-filter', dest='filter', nargs='+', 
                        help="Running tests by defined patterns")
    parser.add_argument("-files", dest="files", nargs='*', default=setting.files,
                        help="files paths or files path paterns")
    args = parser.parse_args(argv)
    return args


if __name__ == "__main__":
    ARGS = parse_args(sys.argv[1:])
    #pytest_options = [f"--files {' '.join(ARGS.files)}"]
    pytest_options = []
    if ARGS.list_tests is not False:
        pytest_options.append("--collect-only")
    if ARGS.np is not None:
        pytest_options.extend(["-n", str(ARGS.np)])
    if ARGS.filter is not None:
        pytest_options.append('-k  "%s"' % ' '.join(ARGS.filter))
    RT = RunTests(pytest_options, log=ARGS.log)
    sys.exit(RT.run())