#!/bin/bash -l

## -l login shell (sets up my user env)

echo
echo "----job.sh----"
echo

OUTDIR=${1}
ARGS=${2}

echo "OUTDIR:  ${OUTDIR}"
echo "ARGS:  ${ARGS}"

cd ${OUTDIR}
#pip install /scratch/grp/epap/k1919811/git/nd280Comp/ 
. /scratch/grp/epap/k1919811/soft/dirac/8.0.21/dirac_ui/diracos/diracosrc


# force python to run in unbuffered mode 
# so that it spits things out to the log as it goes
export PYTHONUNBUFFERED=1
singleJob_nd280Scripts ${ARGS} 

echo 'done'
