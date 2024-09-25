These scripts are currently a bit messy because for the slurm submission you should run   pip install .    in the top directory to get the command/entry point singleJob_nd280Scripts
But for dirac submission, the focus is on packing the necessary files up into the sandbox, which then get put in a flat structure.

Both slurm and dirac should be submitted just by running the ./sub_jobs.py  script with the relevent settings and config files provided.

This setup is temporary while we tranisition to new computing tools.
