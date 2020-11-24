# Exp

This folder contains the all of the code used to run the main experiments of the paper. Note: These scripts operate under the assumption that all of the steps / scripts within Setup have been been run prior. 

### Computation

As these experiments are tremendously computationally expensive, they were run on the University of Vermont's bluemoon supercomputing cluster (https://www.uvm.edu/vacc). This cluster use's a SLURM submission system, so a number of the script within this folder are designed for submitting with SLURM.


### Requiriments

- dask_jobqueue (if planning to use the run.py short queue submissions)