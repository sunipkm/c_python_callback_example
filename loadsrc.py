from ctypes import CFUNCTYPE
from ctypes import c_void_p
from ctypes import POINTER
from ctypes import c_int
from ctypes import cdll
lib = cdll.LoadLibrary('./libsrc.dylib')
CMPFUNC = CFUNCTYPE(c_void_p, POINTER(c_int), POINTER(c_int))

class A:
    def __init__(self, a: int):
        self.a = a
    
    def py_cmp_func(self, s, r):
        print (f'In python: Internal data is {self.a} Quotient is {s[0]} , remainder is {r[0]}')
def py_cmp_func(s, r):
  print (f'Quotient is {s[0]} , remainder is {r[0]}')

x = A(10)

cmp_func = CMPFUNC(x.py_cmp_func)
lib.divide(cmp_func, 3, 5)