# coding: utf8


import runpy


__all__ = ['exec_code', '__version__']

__version__ = '0.0.2.1'


def exec_code(code: str):
    runpy._run_code(code, run_globals=globals())
