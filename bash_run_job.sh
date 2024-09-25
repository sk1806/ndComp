#!/bin/bash -l

## --------
## BASH
## -l login shell (sets up my user env)
## -x debug mode
## -e exit if you hit an error
## export SHELLOPTS - propagate these options to subsequent bash scripts/shells that run frmo this one


## --------
## SBATCH/SLURM
## These would need to be put with one #, #SBATCH, and right below the shebang before any other text

##SBATCH --output=/scratch/grp/epap/k1919811/temp/slurm/%j.out
##SBATCH --error=/scratch/grp/epap/k1919811/temp/slurm/%j.err
## --output/error:  Where to store standard output/error log 

##SBATCH --mem=1G
## Resident memory / RAM 

## NOTE:  
## Using #SBATCH you can use %j (jobid) and %u (user)  (plus someothers)
## Using #SBATCH --output can be good because you can include the jobID in the output filename with %j
## But using sbatch --output can be good to control the output path from your submission script
## Annoyingly you have to chose between these two.


## --------
## Getting slurm vars from bash (slurm sets these for you)
## ${SLURM_JOB_ID}
## ${USER}

echo 
echo "---- bash_run_job.sh ----"  -a  "${OUTDIR}"/slurm_job.log
echo
export SHELLOPTS

echo 
echo "slurm jobid:  ${SLURM_JOB_ID}"  -a  "${OUTDIR}"/slurm_job.log
echo 
scontrol show job ${SLURM_JOB_ID}  -a  "${OUTDIR}"/slurm_job.log
echo
echo "Start: $(date)"  -a  "${OUTDIR}"/slurm_job.log



OUTDIR=${1}
ARGS=${2}
INSAND=${3}


echo "OUTDIR:  ${OUTDIR}"
echo "ARGS:  ${ARGS}"


## Function to take a snapshot of the log file
#snapshot_log() {
#    local log_file="$1"
#    local snapshot_dir="$2"
#    local snapshot_interval="$3"
#
#    while true; do
#        cp "$log_file" "${snapshot_dir}/$(date +%Y%m%d_%H%M%S)_log_snapshot.txt"
#        sleep "$snapshot_interval"
#    done
#}
#
## Your existing script content...

## Call the snapshot_log function in the background
#mkdir -p ${OUTDIR}/logs
#snapshot_log "${OUTDIR}/slurm_job.log" "${OUTDIR}/logs" 3600 &
#SNAPSHOT_PID=$!

RUNDIR=$PWD
/usr/bin/time -v ${RUNDIR}/job.sh "${OUTDIR}" "${ARGS}"  2>&1 | tee -a  "${OUTDIR}"/slurm_job.log

sleep 80
echo $(sacct -j $SLURM_JOB_ID --format=JobID,MaxVMSize,MaxRSS,Elapsed) 2>&1 | tee -a  ${OUTDIR}/slurm_job.log

echo "End: $(date)"  -a  "${OUTDIR}"/slurm_job.log

#kill $SNAPSHOT_PID

