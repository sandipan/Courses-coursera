#!/usr/bin/env python3
# ///////////////////////////////////////////////////////////////////////////////////////////
#   Usage:
#           python timing.py -nt T
#           T:   number of iterations to run for (default = 1000)
#
#   Description:
#           Computes a[1:nx] = -a[1:nx] T times (nx = 10256)
#           Reports time
#           Reports average time per iteration
#           Reports average time per iteration per point

def main():
    from time import time
    import numpy as np
    import argparse

    # Read command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-nt', type=int, default=1000,
                        help='Number of iterations the calculation is performed')
    parser.add_argument('-nx', type=int, default=1000,
                        help='Number of elements in array')
    args = parser.parse_args()
    niter = args.nt
    nx = args.nx

    # ////////////////////////////////
    # Initialize
    a = np.zeros(nx, dtype='float64')
    b = np.zeros(nx, dtype='float64')
    c = np.zeros(nx, dtype='float64')
    r = np.zeros(nx, dtype='float64')

    a[:] = 1.0
    b[:] = 2.0
    c[:] = 5.0

    # Loop (and time)
    loop_start = time()

    for n in range(niter + 1):
        r[:] = a[:]*b[:]+c[:]

    loop_end = time()
    walltime = loop_end - loop_start

    print(' Number of points: ', nx)
    print(' Number of iterations:   ', niter)
    print(' Elapsed time: ', walltime)
    print(' Elapsed time per iteration: ', walltime / float(niter))
    print(' Elapsed time per iteration per point: ', walltime / float(niter) / float(nx))


#############################
if (__name__ == "__main__"):
    main()
