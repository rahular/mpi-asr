import random
import time
import os
import subprocess
import sys

import numpy as np

from mpi4py import MPI

comm = MPI.COMM_WORLD
num_workers = 8
multipliers = 1000000

def master():
    final_result = []

    # send inputs to slaves
    for i in range(1, num_workers):
        packet = { 'input': i }
        comm.send(packet, dest=i)

    # recieve results from slaves
    for i in range(1, num_workers):
        result_packet = comm.recv(source=i)
        final_result.append(result_packet)

    print('Final result shape: {}'.format(np.array(final_result).shape))


def slave():
    # each slave will return a table of numbers
    packet = comm.recv(source=0)
    result_packet = [packet['input'] * i for i in range(1, multipliers+1)]
    comm.send(result_packet, dest=0)


def main():
    rank = comm.Get_rank()
    start_time = time.time()

    if rank == 0:
        master()
        end_time = time.time()
        print('Total time elapsed for master {}: {}'.format(rank, end_time - start_time))
    elif rank > 0:
        slave()
        end_time = time.time()
        print('Total time elapsed for slave {}: {}'.format(rank, end_time - start_time))


if __name__ == '__main__':
    main()
