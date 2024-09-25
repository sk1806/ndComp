#!/usr/bin/env python

import argparse
import os

# Temp setup, to allow for installed package and scripts shoved in sandbox in a flatstructure
try:
    from nd280Jobs import nd280Scripts
except ImportError:
    import nd280Scripts



def parse_arguments():
    """
    Parses and return command line arguments.
    """

    parser = argparse.ArgumentParser(description='Job type and input')
    
    parser.add_argument('--image', dest='image', action='store', required=True,
                        help='path to image on CVMFS')
     
    parser.add_argument('--job', dest='jobType', action='store', default='custom', required=True,
                        choices = ['nd280sc_neutSetup', 'nd280sc_neutMC', 'nd280sc_nd280chain', 'nd280sc_calib_ecal', 'nd280sc_custom', 'custom'],
                        help='Job type can be:  nd280sc_neutMC, nd280sc_nd280chain, nd280sc_custom, custom')
       
    parser.add_argument('--inputfile', dest='inputfile', action='store', required=False,
                        help='Supply input file if required')     
    
    parser.add_argument('--gridout', dest='gridOutPath', action='store', required=False,
                        help='Supply grid output path if required')
    
    parser.add_argument('--run', dest='runNum', action='store', required=False,
                        help='Supply run number if required')
    
    parser.add_argument('--subrun', dest='subrunNum', action='store', required=False,
                        help='Supply subrun number if required')

    parser.add_argument('--configtemp', dest='configtemp', action='store', required=False,
                        help='Specify the temp config file (path and filename), rather than using the default ./job_temp.cfg ')

    parser.add_argument('--bindpaths', dest='bindpaths', action='store', required=False,
                        help='Specify additional binding paths for the container')


    return parser.parse_args()



def main():

    # loop - inputfilelist/numrange
    #
    #  single job
    #    image
    #    gridloc
    #    cfg
    #    inputfile/number

    args = parse_arguments()
    print('------ singleJob_nd280Scripts.py ------')
    print('singleJob_nd280Scripts  args:  ' + str(args))

    j = nd280Scripts.nd280Job(args.image, args.jobType )


    if args.bindpaths:
        j.setBindPaths(args.bindpaths)
 

    ## Legacy For P6
    j.setSetup(
        'export CMTPATH=/usr/local/t2k/current/nd280/; '
        'export CMTROOT=/usr/local/t2k/current/CMT/CMT/v1r20p20081118/; '
        'source /usr/local/t2k/current/nd280/nd280/*/cmt/setup.sh'
    )
    
    if args.runNum and args.subrunNum:
        print('singleJob_nd280Scripts:  setRunSubrun')
        j.setRunSubrun(args.runNum, args.subrunNum)   
    
    if args.inputfile:
        j.setInputFile(args.inputfile)
        # nd280 expects numc to be in the same directory

        if not args.inputfile.startswith('/t2k.org') and not args.inputfile.startswith('/cvmfs') :
            if args.jobType == "nd280sc_nd280chain": # or args.jobType == "nd280sc_calib_ecal" :  # flux for neutSetup doesn't seem to like the linking
                com_cp = f"ln -s {args.inputfile} ./"
                print(f"Linking  {args.inputfile} to $PWD")
                print(com_cp)
                os.system(com_cp)
    if args.configtemp:
        j.setConfigTemp(args.configtemp)
    j.FillND280Config()
    #nd280Scripts.nd280Job.FillND280Config(j) 
    
####      j.setRunCom('''\
####  export JOB="runND280 -c job.cfg"
####  echo "#!/bin/bash" > valgrindJob.sh
####  echo "${JOB}" >> valgrindJob.sh
####  chmod +x ./valgrindJob.sh
####  ###valgrind --tool=callgrind ./valgrindJob.sh
####  valgrind ./valgrindJob.sh
####  PID=$!
####  ###sleep 1h
####  ###kill -SIGTERM $PID
####  ###wait $PID
####      ''')

    j.runInsideContainerScript()
        
    if args.jobType == 'nd280sc_calib_ecal':
        subsuffix = 'ecalmod'
    else:
        subsuffix = ''       
     
    print('About to run runOutsideContainerScript')
    print(args.gridOutPath, subsuffix)
    j.runOutsideContainerScript(args.gridOutPath, subsuffix) 
    
    com_chmod = 'chmod +x *.sh*'
    os.system(com_chmod)
    com_run = './run_nd280_outsideContainer.sh'
    os.system(com_run)


if __name__ == '__main__':
    main()
