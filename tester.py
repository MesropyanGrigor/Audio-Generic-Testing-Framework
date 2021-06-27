"""Generic testing framework"""
import argparse
import sys
import shlex
import subprocess

#import Krisp.settings

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', dest='config',
                        help="Config file path")
    parser.add_argument('-np', dest='np', type=int,
                        help=("Running in parallel mode, "
                              "using provided value as number of cores"))
    parser.add_argument('-l', dest='list_tests', action="store_true", 
                        help="Show available tests")
    parser.add_argument('-log', dest='log', 
                        help="Keep pytest output into that log file")
    # add -l option to show available list of test
    args = parser.parse_args(argv)
    return args


if __name__ == "__main__":
    ARGS = parse_args(sys.argv[1:])
    pytest_options = ['--tb=no']
    if ARGS.list_tests is not False:
        pytest_options.append("--collect-only")
    else:
        pytest_options.append('--durations=0 -vv')
    if ARGS.np is not None:
        pytest_options.extend(["-n", str(ARGS.np)])
    RT = RunTests(pytest_options, log=ARGS.log)
    RT.run()