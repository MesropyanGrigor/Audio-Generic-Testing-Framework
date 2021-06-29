import pytest

def pytest_addoption(parser):
    parser.addoption("--files", dest='files', nargs='*',
                     help="files paths or files path paterns")





