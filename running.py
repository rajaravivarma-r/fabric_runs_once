"""Decorator to limit a function execution to once in multiprocessing environment"""

from __future__ import print_function
import os
import errno
from functools import wraps

def runs_once(marker, error_msg=None):
    """Use this function as decorator to run a method only once in multiprocessing environment"""
    def deco_lock(func):
        @wraps(func)
        def func_decorator(*args, **kwargs):
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            try:
                file_handle = os.open(marker, flags)
                os.close(file_handle)
                func(*args, **kwargs)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    if error_msg:
                        print(error_msg)
                else:
                    raise e
        return func_decorator
    return deco_lock
