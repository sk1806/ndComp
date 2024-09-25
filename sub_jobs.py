#!/usr/bin/env python

import os
import glob
import subprocess
import re
from datetime import datetime
import json
import shutil
import time

from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac

from  nd280Jobs import nd280Scripts


def main():


    ####################################################################
    ########### Initialize some variables to default values ############
    ####################### Do NOT edit this bit #######################

    slurmfolder = None
    bindpaths = None


    sub_single = False
    ## inputfile = ''

    sub_loopRunSubrun = False
    ### Z : 9 -> Neutrino MC, 8 -> Anti-neutrino MC
    ### A = Generator (0: NEUT, 1: GENIE, 2: old NEUT)
    ### B = ND280 Data Run (with a certain beam condition and set of dead channels assumed for each run)
    ### C = 0: P0D air, 1: P0D water
    ### D = Volume / Sample type (0: Magnet, 1: Basket (beam), 2: nue, 3: NC1pi0, 4: CC1pi0, 5: NC1pi+, 6: CC1pi+, 7: tpcgas)
    ### E = MC Run number
    ##code = 90400  ### XXX NEW RUN NUMBERING SCHEME !?!?!? ### XXX
    ##run_min = 0
    ##run_max = 1 #300 #129 #129
    ##subrun_min = 0
    ##subrun_max = 56 #56
    ## inputfile = ''

    sub_filelist = False
    ## filelist = ''   
    
    sub_numlist = False
    ## inputfile = ''
    ## in_numlist = ''

    ## Optional - used for sand
    NameFromEnd = False
    precode = '99999'  
    setRun = ''
    setSubrun = ''

    # Optional
    insand = None

    ####################################################################



    ##################################################################
    ###################### START OF STUFF TO EDIT ####################
    ##################################################################

    ## TODO - Just handle this bit with a job input cards rather than editting this script

    ## Pick one of the examples that matches the type of job you want to submit
    ## neutSetup, neutMC, nd280chain, calib_ecal
    ##
    ## Make sure you set 'sub' to 'dirac' or 'slurm' as shown in the examples
    ##
    ## e.g. dirac
    ## sub = 'dirac'
    ## 
    ## e.g. slurm
    ## sub = 'slurm'
    ## bindpaths = '/scratch/grp/epap/'  
    ## slurmfolder = datetime.now().strftime("%Y%m%d_%H%M%S")
    ##
    ##################################


    ############################
    #### neutSetup example #####
    ############################
    ## P8 V04 2924 neut_5.6.4.3_p7c3 FHC 23av1 320kA - neutSetup
    #
    ## Settings for local slurm submission
    #sub = 'slurm'
    #bindpaths = '/scratch/grp/epap/'  
    #slurmfolder = datetime.now().strftime("%Y%m%d_%H%M%S")    
    #outpath = '/scratch/grp/epap/k1919811/create_batch_out/nd280/production008/testing25_event_rate'
    #image = '/cvmfs/t2k.egi.eu/nd280_containers/nd280softwaremaster_almalinux9.4-14.25_sand'
    #inputfile = '/scratch/grp/epap/scratch/t2k/grid/t2k.org/beam/mc/beamMC/flux23av1_2024/hadded/flux23av1_p320_nd6_newtargetmc_run13_hadd__root-5-34-09_remove_Enu0.root'
    #
    ## Settings for dirac submission
    #sub = 'dirac'
    #outpath = '/t2k.org/user/k/sophie.king
    #image = '/cvmfs/t2k.egi.eu/nd280_containers/nd280softwaremaster_almalinux9.4-14.25_sand'
    #inputfile = '/t2k.org/whatever/file
    #
    ## Job Seetings - independent of slurm or dirac
    #job_type = 'nd280sc_neutMC'  #'nd280sc_neutSetup' #'nd280sc_neutMC'  #'nd280sc_nd280chain' #'nd280sc_calib_ecal 
    #sub_single = True
    #cfg = './nd280sc_cfg/prod/p8_val/p8_V04_neut_5.6.4.3_p7c3_neutSetup_2024__23av1_p320__runA.cfg'
    #neut_card = './neut_cards/neut.5.6.4.3_p7c3.card'
    #insand = [neut_card, cfg]


    ########################
    #### neutMC example ####
    ########################
    ## P8 V02  2024 neut_5.6.4.1_p7c3 FHC-13a-250kA  - neutMC
    #
    #sub = 'dirac'
    #job_type = 'nd280sc_neutMC'  #'nd280sc_neutSetup' #'nd280sc_neutMC'  #'nd280sc_nd280chain' #'nd280sc_calib_ecal '
    #image = '/cvmfs/t2k.egi.eu/nd280_containers/nd280softwaremaster_almalinux9.4-14.23_sand'
    #outpath = '/t2k.org/user/k/sophie.king/nd280/production008/validation/V02/mcp/neut_5.6.4.1_p7c3/2024/magnet/13a_p250kA/runA'
    #cfg = './nd280sc_cfg/prod/p8_val/p8_V02_neut_5.6.4.1_p7c3_neutSetup_2024__13a_p250__runA.cfg'
    #inputfile = '/t2k.org/nd280/production008/validation/V02/mcp/neut_5.6.4.1_p7c3/2024/magnet/13a_p250kA/evtr/evtr/p8_V02_neut_5.6.4.1_p7c3_neutSetup_2024__13a_p250__evtr.root'
    #insand = ['neut_cards/neut.5.6.4.1_p7c3.card', cfg]
    ####
    ########### Z : 9 -> Neutrino MC, 8 -> Anti-neutrino MC
    ########### AB = ND280 Data Run (with a certain beam condition and set of dead channels assumed for each run)
    ########### C = 0: P0D air, 1: P0D water 2: upgrade
    ########### D = Volume / Sample type (0: Magnet, 1: Basket (beam), 2: nue, 3: NC1pi0, 4: CC1pi0, 5: NC1pi+, 6: CC1pi+, 7: tpcgas)
    ########### E = MC Run number
    ####
    ####
    #### sub number loop ####
    ####
    #sub_loopRunSubrun = True
    #code = 90020  ### XXX NEW RUN NUMBERING SCHEME !?!?!? ### XXX
    #run_min = 30 #0
    #run_max = 50 #129 #300 
    #subrun_min = 0 #0
    #subrun_max = 56 #56
    ####
    ####
    #### sub list of (missing) numbers ####
    ####
    #sub_numlist = True
    #in_numlist = '/scratch/grp/epap/k1919811/git/nd280Comp/old_t2k_stuff/p8_V02_p250ka/numc_dfc_mis.list'
    ##########


    ############################
    #### nd280 chain example ###
    ############################
    ##p8 mini prod 
    ##
    #sub = 'slurm'
    #bindpaths = '/scratch/grp/epap/'
    #slurmfolder = datetime.now().strftime("%Y%m%d_%H%M%S")
    #outpath = '/scratch/grp/epap/k1919811/create_batch_out/nd280/production008/testing25'
    #filelist = 'lists/p8_V02_neut_5.6.4.1_p7c3_2024_13a_p250_numc_kcl.list'  
    #
    #job_type = 'nd280sc_nd280chain' 
    #image = '/cvmfs/t2k.egi.eu/nd280_containers/nd280softwaremaster_almalinux9.4-14.24_sand'
    #cfg = './nd280sc_cfg/prod/p8_val/p8_V04_neut_5.6.4.1_p7c3_2024_p250kA_nd280_runA.cfg'
    #sub_filelist = True
    #neut_card = 'neut_cards/neut.5.6.4.3_p7c3.card'
    #tag = 'nd280_tags/blank.txt'
    #insand = [neut_card, tag, cfg]



    ############################
    #### ecal calib example ####
    ############################
    ##
    ## Settings for submitting locally to slurm
    #sub = 'slurm'
    #bindpaths = '/scratch/grp/epap/'
    #slurmfolder = datetime.now().strftime("%Y%m%d_%H%M%S")
    #outpath = '/scratch/grp/epap/k1919811/create_batch_out/calib/test_a'
    #filelist = 'lists/nd280_midas_00010000_00010999_1file_kcl.list' 
    ##
    ## Settings for submitting to dirac
    sub = 'dirac'
    outpath = '/t2k.org/user/k/sophie.king/calib/test_d'
    filelist = 'lists/nd280_midas_00010000_00010999_1file.list' 
    ##
    ## Job settings indepdendent of dirac or slurm
    job_type = 'nd280sc_calib_ecal'  #'nd280sc_neutSetup' #'nd280sc_neutMC'  #'nd280sc_nd280chain' #'nd280sc_calib_ecal '
    image = '/cvmfs/t2k.egi.eu/nd280_containers/nd280softwaremaster_almalinux9.4-14.25_sand'
    cfg = 'nd280sc_cfg/calib/calib_ecal_temp.cfg'
    sub_filelist = True
    ecal_dat_mod = "calib_dat/ECALMOD.PARAMETERS.DAT"
    ecal_date_widetimecut = "calib_dat/ECALWIDETIMECUT.PARAMETERS.DAT"
    insand = [cfg, ecal_dat_mod, ecal_date_widetimecut]


    ##################################################################
    ###################### END OF STUFF TO EDIT ######################
    ##################################################################




    # This is the job loop
    # This is a bit of a messy way to do it.. plan to reorganize
    if (sub_loopRunSubrun):
        time.sleep(1)
        for i in range(run_min, run_max):
            for k in range( subrun_min, subrun_max):
                submit_dirac_slurm(sub, image, job_type, outpath, inputfile, str(code) +str(i).zfill(3), str(k).zfill(4), insand, cfg, slurmfolder)
    elif (sub_numlist):
        f_in = open(in_numlist, 'r')
        for line in f_in:
            time.sleep(1)
            print(line)
            numbers = line.rstrip('\n').split(' ')
            print(numbers)
            run = numbers[0]
            subrun = numbers[1]
            submit_dirac_slurm(sub, image, job_type, outpath, inputfile, run , subrun, insand , cfg, bindpaths, slurmfolder)
    elif(sub_single):
        submit_dirac_slurm(sub, image, job_type, outpath, inputfile, '', '', insand, cfg, bindpaths, slurmfolder)
    elif(sub_filelist):
        f_in = open(filelist, 'r')
        for input_file in f_in:
            #time.sleep(1)
            run = ''
            subrun = ''
            if(NameFromEnd):   
                ## TODO I can't remember why I put this in here on top of what is done inside submit_slurm and submit_dirac
                ## And I can't remember the use case of setRun and setSubrun
                ## There were reasons...
                if setRun == '':     run = nd280Scripts.GetRunNumFromNameEnd(input_file, 3, precode )
                else:  run = setRun
                if setSubrun == '':  subrun = nd280Scripts.GetSubrunNumFromNameEnd(input_file, 4)
            submit_dirac_slurm(sub, image, job_type, outpath, input_file, run, subrun, insand, cfg, bindpaths, slurmfolder)




def submit_dirac_slurm(which, image, job_type, outpath, input_file, run, subrun, insand, cfg, bindpaths, slurmfoldername):
    if which == 'dirac':
        return submit_dirac(image, job_type, outpath, input_file, run, subrun, insand, cfg, bindpaths)
    elif which =='slurm':
        return submit_slurm(image, job_type, outpath, input_file, run, subrun, insand, cfg, bindpaths, slurmfoldername)
    else:
        raise ValueError('Need to choose a valid submission: dirac or slurm')


def create_slurm_command(job_name, outdir, datetime_str,  script, script_arg1, script_arg2):
    # Split the args string into a list of arguments
    sbatch_command = [
        "sbatch",
        f"--partition=nmes_cpu",
        f"--job-name={job_name}",
        f"--mem=20G",
        f"--output={os.path.join(outdir, f'slurm_{datetime_str}.out')}",
        f"--error={os.path.join(outdir, f'slurm_{datetime_str}.err')}",
        f"--time=48:00:00",
        script,
        script_arg1,
        script_arg2
    ] 
    return sbatch_command



def submit_slurm(image, job_type, localoutpath, input_file=None, run=None, subrun=None, insand=None, configtemp=None, bindpaths=None, foldername=None):
    """
    Function to submit the job to SLURM
    - image is the singularity container image/sandbox
    - job_type must be passed so that the job will set up the script properly and then also know which files to upload
    - localoutpath is the base location where the job will run
    - foldername is the name of the folder within the localoutpath.  Defaults to a datetime stamp to ensure unique folders.
    - input_file, run and subrun are filled for some job_type and empty for other job_type
    - insand provides the option to add one (string) or more (list of strings) items to the input sandbox
    - configtemp is the name of the config file template before it is filled.  If not specified then job_temp.cfg
    """

    args = f" --image {image}  --job {job_type}  --configtemp {os.path.basename(configtemp)}"
    if (input_file):
        print(f"input file: {input_file}")
        args = f"{args}  --input {input_file}"
    if( run and subrun ):
        args = f"{args} --run {run}  --subrun {subrun}"
    if(bindpaths):
        args = f"{args}  --bindpaths {bindpaths}"
    print(f"{args}:  {args}")

    job_name = job_type
    if (run and subrun):
        job_name = f"{job_type}_{run}-{subrun}"
    else:
        if(input_file):
            if job_type == 'nd280sc_calib_ecal':
                run = nd280Scripts.GetRunNumFromNameEnd(input_file)
                subrun = nd280Scripts.GetSubrunNumFromNameEnd(input_file)
            else:
                run = nd280Scripts.GetRunNumFromName(input_file)
                subrun = nd280Scripts.GetSubrunNumFromName(input_file)
            job_name = f"{job_type}_{run}-{subrun}"
            print(f"job_name = {job_name}")

    # Get current date and time
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the job/out directory
    if(foldername is None):
        foldername = datetime_str
    outdir = os.path.join(localoutpath, foldername, job_name)
    os.makedirs(outdir, exist_ok=True)

    # copy input sandbox to the job/out directory
    for filepath in insand:
        #if filepath.startswith('/t2k.org') .. add something to download it?
        shutil.copy(filepath, os.path.join(outdir, os.path.basename(filepath)))

    # submit slurm job
    print(f"Slum outdir: {outdir}")
    slurm_command = create_slurm_command(job_name, outdir, datetime_str, "bash_run_job.sh", outdir, args)
    result = subprocess.run(slurm_command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error submitting job: {result.stderr}")
    # Extract job ID
    job_id = re.search(r'\d+', result.stdout).group()
   
    with open(os.path.join(outdir, f"slurm_jobid_{job_id}__datetime_{datetime_str}.log"), 'w') as log_file:
        log_file.write(f"Submitted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"SLURM Job ID: {job_id}\n\n")
        log_file.write("SLURM Job:\n")
        log_file.write(' '.join(slurm_command) + '\n\n' )   

    # Write just the job ID to a separate file
    # Can be useful for bookeeping and writing other tools/monitoring
    job_id_filename = f"slurm_jobid_{job_id}__datetime_{datetime_str}.id"
    with open(os.path.join(outdir, job_id_filename), 'w') as id_file:
        id_file.write(str(job_id))




def submit_dirac(image, job_type, gridoutpath, input_file=None, run=None, subrun=None, insand=None, configtemp=None, bindpaths=None ):
    """
    Function to submit the job to DIRAC
    - image is the singularity container image/sandbox
    - job_type must be passed so that the job will set up the script properly and then also know which files to upload
    - gridoutpath is the base location where files will be uploaded to the grid
    - input_file, run and subrun are filled for some job_type and empty for other job_type
    - insand provides the option to add one (string) or more (list of strings) items to the input sandbox
    - configtemp is the name of the config file template before it is filled.  If not specified then job_temp.cfg
    """
    ## TODO - log the JID numbers

    # Arguments for singleJob_nd280Scripts.py
    args = f" --image {image}  --job {job_type}  --gridout {gridoutpath}"
    if(configtemp):
        args = f'{args}  --configtemp "{os.path.basename(configtemp)}"'
    if(input_file):
        args = f"{args}  --input {input_file}"
    if(run and subrun):
        args = f"{args}  --run {run} --subrun {subrun}"
    if(bindpaths):
        args = f"{args}  --bindpaths {bindpaths}"

    print(f"args:  {args}")

    # Create the input sandbox
    # The list of files that get packed up and sent with the job
    input_sandbox = [
        "nd280Jobs/nd280Scripts.py",
        "nd280Jobs/singleJob_nd280Scripts.py",
        "jobTools/seedGenerator.py",
        "upload_search.py",
        "update_status.py",
        "gridTools.py",
        "jobTools/check_nRooTracker.py",
        "jobTools/pyrootTools.py",
        "jobTools/fileTools.py"
    ]
    # user specificed part of sandbox
    if(insand):
        if isinstance(insand, str):
            # insand could be a single string or a list of strings
            insand = [insand]
        input_sandbox = input_sandbox + insand
    print(f"input_sandbox:  {input_sandbox}")
    # Add LFN: at the front so DIRAC recognizes that it needs to download it
    if input_file.startswith("/t2k.org"):
        if(input_file):
            if('LFN:' in input_file):
                LFN = input_file
            else:
                LFN = f"LFN:{input_file}"
            input_sandbox.append(LFN)

    # Create the name for the job in the DIRAC server
    job_name = job_type
    if (run and subrun):
        job_name = f"{job_type}_{run}-{subrun}"
    else:
        if(input_file):
            print(f"sub_jobs.py submit_dirac:  Getting run and subrun from input file {input_file}")
            if job_type == 'nd280sc_calib_ecal':
                run = nd280Scripts.GetRunNumFromNameEnd(input_file)
                subrun = nd280Scripts.GetSubrunNumFromNameEnd(input_file)
            else:
                run = nd280Scripts.GetRunNumFromName(input_file)
                subrun = nd280Scripts.GetSubrunNumFromName(input_file)
            print(f"run = {run}")
            print(f"subrun = {subrun}")
            job_name = f"{job_type}_{run}-{subrun}"
            print(f"job_name = {job_name}")

    
    # Submit job to DIRAC
    j = Job()
    j.setName(job_name)
    j.setJobGroup(job_type)
    j.setCPUTime(300000)
    j.setInputSandbox(input_sandbox)
    j.setOutputSandbox([ "StdErr" , "StdOut", "nd280.log", "upload.log","job.cfg", "run_nd280_insideContainer.sh", "run_nd280_outsideContainer.sh"])
    j.setExecutable("./singleJob_nd280Scripts.py", arguments=args, logFile="job.log")
    #j.setBannedSites([ 'LCG.UKI-SCOTGRID-GLASGOW.uk'])
    #j.setDestination('LCG.UKI-LT2-QMUL.uk')
    #j.setDestination('LCG.RAL-LCG2.uk')
    #j.setDestination('LCG.IN2P3-CC.fr')
    #j.setDestination('LCG.UKI-LT2-IC-HEP.uk')
    #j.setDestination('LCG.UKI-SCOTGRID-GLASGOW.uk')
    #j.setDestination('LCG.UKI-NORTHGRID-SHEF-HEP.uk')
    #j.setDestination('LCG.UKI-NORTHGRID-LIV-HEP.uk')
    #j.setDestination('LCG.UKI-NORTHGRID-LANCS-HEP.uk')
    #j.setDestination('LCG.NCBJ-CIS.pl')
    print('')
    res = Dirac().submitJob(j)
    print(res['OK'])
    print(res['JobID'])
    print('-- \n')


if __name__ == "__main__":
    main()

   
