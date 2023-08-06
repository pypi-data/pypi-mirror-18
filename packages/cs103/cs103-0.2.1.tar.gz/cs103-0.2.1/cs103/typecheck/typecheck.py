from typing import *
from enum import Enum
import os
import sys
import traceback
import inspect

class TypecheckError(TypeError):
    def __init__(self, val, a, b, fn):
        self.fn = fn
        return super().__init__('\x1b[32m%s\x1b[0m is a \x1b[36m%s\x1b[0m, not a \x1b[36m%s\x1b[0m'%(val,a,b))
    def _render_traceback_(self):
        print('\x1b[31m')
        print('-'*75)
        print(type(self).__name__)
        print('\n' + str(self) + '\n')
        print(traceback.format_tb(sys.exc_info()[2])[1])
        print('as expected in\n\x1b[34m')
        print(''.join(['  ' + x for x in inspect.getsourcelines(self.fn)[0]]))
        print('\x1b[0m')

class ReturnError(TypecheckError):
    def __init__(self, te):
        self.te = te
        return None
    def _render_traceback_(self):
        print('\x1b[31m')
        print('-'*75)
        print(type(self).__name__)
        print('\nreturned value ' + str(self.te) + ' as expected in\n\x1b[34m')
        print(''.join(['  ' + x for x in inspect.getsourcelines(self.te.fn)[0]]))
        print('\x1b[0m')


def subtype(va: any, tb: any, fn: any = None, strict: bool = False) -> bool:
    ta = type(va)
    
    if issubclass(tb, Union):
        if not (ta == tb or any(subtype(va,t,fn) for t in tb.__union_params__)):
            raise TypecheckError(va,ta.__name__,tb.__name__, fn)
    elif issubclass(tb, List):
        if ta is not list:
            raise TypecheckError(va,ta.__name__,tb.__name__, fn)
        all(subtype(v, tb.__args__[0], fn, True) for v in va)
    elif tb is float:
        rv = ta is int or ta is float
        if strict and not rv:
            raise TypecheckError(va,ta.__name__,tb.__name__, fn)
        return rv
    elif ta != tb:
        if strict:
            raise TypecheckError(va,ta.__name__,tb.__name__, fn)
        return False
        
    return True

def typecheck(fn):
    def wrapper(*args):
        types = get_type_hints(fn)
        for name, val in zip(fn.__code__.co_varnames, args):
            subtype(val, types[name], fn, True)

        retval = fn(*args)
        try:
            subtype(retval, types['return'], fn, True)
        except TypecheckError as e:
            raise ReturnError(e)

        return retval
    return wrapper
