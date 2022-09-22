from __future__ import annotations
from ctypes import CFUNCTYPE
from ctypes import c_void_p
from ctypes import c_char_p
from ctypes import c_void_p
from ctypes import POINTER
from ctypes import c_int
from ctypes import c_char
from ctypes import c_size_t
from ctypes import c_bool
from ctypes import byref
from ctypes import cdll
from ctypes import c_int
from ctypes import cast

import numpy as np

import platform

os_type = platform.system()

ext = ''
if os_type.lower() == 'linux':
    ext = '.so'
elif os_type.lower() == 'darwin':
    ext = '.dylib'
else:
    raise RuntimeError('Platform %s not known.'%(os_type))

lib = cdll.LoadLibrary('./libsrc' + ext)
LIBSRC_CALLBACK_FUNC_TYPE = CFUNCTYPE(None, c_char_p, c_size_t, c_char_p, c_size_t)

lib.actor_new.argtypes = LIBSRC_CALLBACK_FUNC_TYPE,
lib.actor_new.restype = POINTER(c_void_p)

class actor:
    def __init__(self, py_func):
        self._handle = lib.actor_new(LIBSRC_CALLBACK_FUNC_TYPE(py_func))

    def __del__(self):
        lib.actor_destroy(byref(self._handle))

def fcn(input, input_len, input2, input2_len):
    # buf = np.zeros((input_len), dtype = np.int8)
    # buf.ctypes.data_as(input)
    print('In python: %s | %s'%(input.decode('utf-8'), input2.decode('utf-8')))


import time
x = actor(fcn)
time.sleep(5)
del x

    
