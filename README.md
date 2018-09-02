# es-deepspeech

Utilities to run deep speech as a REST API and some MPI tests.

## Run deep speech server
Install the requirements and run `python deepspeech-server.py`.
API client code snippet is available in `deepspeech-client.py`.

## Running MPI tests:
To know more about what MPI is, see [here](https://mpi4py.readthedocs.io/en/stable/intro.html).
First run the script `install-mpi4py.sh` to install all dependencies (tested only for mac).
Then run `mpi-test.py` with the following command: `mpirun -np 8 python mpi-test.py`.

The `np` flag denotes the number of parallel workers (1 master and 7 slaves).
If you want to change the number of workers, change the value of `np` and change the `num_workers` variable inside the code (both should have the same value)

If everything goes well, you should get an output like this:
```
Total time elapsed for slave 1: 0.28195691108703613
Total time elapsed for slave 2: 0.33805084228515625
Total time elapsed for slave 3: 0.3919670581817627
Total time elapsed for slave 4: 0.44113707542419434
Total time elapsed for slave 5: 0.48983216285705566
Total time elapsed for slave 6: 0.5376040935516357
Total time elapsed for slave 7: 0.589820146560669
Final result shape: (7, 1000000)
Total time elapsed for master 0: 1.1907389163970947
```
