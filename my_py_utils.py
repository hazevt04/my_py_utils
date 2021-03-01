#!/usr/bin/env python3

# Utility Methods

import numpy as np
import random
from array import *
import math as m
import time

from functools import reduce
import sys
import os
cpath = os.getcwd()
sys.path.append(cpath)

def debug_func(debug, func_name, *args):
    if debug:
      func_name(*args)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print("{}(): {} ms".format(method.__name__, (te-ts)*1000))
            #%r  %2.2f ms' % \
            #      (method.__name__, (te - ts) * 1000)
        return result
    return timed


def average(vals): 
  return reduce(lambda a, b: a + b, vals) / len(vals)


def gen_random_complex_vals( num_vals, debug=False ):
    rand_comps = np.random.rand( num_vals, 2 )
    return rand_comps.view(dtype=np.complex)


def rand_complex_vals_to_file( filename, num_vals, debug=False ):
    with open( filename, "wb"  ) as ifile:
      rcs = gen_random_complex_vals( num_vals, debug )
      for rc in rcs:
          ifile.write( rc )


def gen_random_floats( num_floats ):
    return [random.uniform(val, 100) for val in range(num_floats) ]


def write_binary_floats( floats, bfilename ):
    with open( bfilename, 'wb' ) as bfile:
        float_array = array( 'f', floats )
        float_array.tofile(bfile)


def read_binary_floats( num_vals, bfilename ):
    with open( bfilename, 'rb' ) as bfile:
        num_val_bytes = np.dtype(np.float32).itemsize * num_vals
        float_array = array('f')
        float_array.frombytes(bfile.read( num_val_bytes ))
        return float_array


if __name__ == '__main__':
    num_vals = (1<<20)
    debug = False
    print("Generared {} random complex values:".format(num_vals))
    random_complex_vals = gen_random_complex_vals( num_vals, debug )
    print("First 10 random complex values:\n{}".format(random_complex_vals[:10]))

    print("Generared {} random floats:".format(num_vals))
    random_floats = gen_random_floats( num_vals )
    
    print("First 10 random floats:\n{}".format(random_floats[:10]))
    filename = "my_floats.bin"

    write_binary_floats( random_floats, filename )
    print("Wrote {} random floats to {}".format(num_vals, filename) )
    
    read_vals = read_binary_floats( num_vals, filename )
    print("Read {} random floats to {}".format(num_vals, filename) )

    print("First 10 floats read from file:\n{}".format(read_vals[:10]))

    max_diff = 0.1
    for i in range(num_vals):
        if not m.isclose( read_vals[i], random_floats[i], abs_tol=max_diff ):
            print("Mismatch betwen read_val {}: {}".format(i, read_vals[i]))
            print(" and random_floats {}: {}".format(i, random_floats[i]))
            exit()

    print("All {} floats were close (within {} of) the floats read back from {}".format(num_vals, max_diff, filename))



