#!/usr/bin/env python3

import os
import sys
import fileinput
import optparse
import re

# This is a temporary way of doing things, to handle pip install
# as well as packing python files into dirac sandbox
try:
    from jobTools import seedGenerator
except ImportError:
    import seedGenerator


class nd280Job(object):
    """ Base class for all types of ND280 Job: Raw data, beam MC etc etc"""

    def __init__(self, image, jobType):
        self.jobType    = jobType
        #self.numcInputFile  = ''
        #self.midInputFile = ''
        self.runNum = ''
        self.subrunNum = ''
        self.inputFile = ''
        self.setup      = ''
        self.runCom     = ''
        self.jobFolder  = './'   ## not used yet
        self.image      = image
        self.configTemp = 'job_temp.cfg'
        self.configFilled = 'job.cfg'
        self.binds      = ''

    def setSetup(self, setup=None):
        if(setup):   
            self.setup = setup
            print('Setting setup script: ' + setup)
        return 

    def setRunCom(self, runCom=None):
        if(runCom): 
            self.runCom = runCom
        elif self.runCom != '':  # if already set, do nothing
            pass
        elif 'nd280sc' in self.jobType:
            self.runCom = 'runND280 -c ' + self.configFilled
        print('Run command set: ' + self.runCom)

    #def setNumcInputFile(self, numcInputFile = ''):
    #    self.numcInputFile = numcInputFile	

    #def setMidInputFile(self, midInputFile = ''):
    #    self.midInputFile = midInputFile	

    def setInputFile( self, inputFile = '' ):
        self.inputFile = inputFile
        print('Setting input file:  ' + inputFile)
	
    def setRunSubrun(self, run = '', subrun = ''):
        print('nd280Scripts:  setRunSubrun')
        print('Setting run:  ' + run)
        print('Setting subrun:  ' + subrun)
        self.runNum = run
        self.subrunNum = subrun
        print('Set run:  ' + self.runNum)
        print('Set subrun:  ' + self.subrunNum)

    def setConfigTemp(self, configTemp = ''):
        print('\nSetting configTemp')
        if configTemp != '':     # if supplied in function, set it
            self.configTemp = configTemp
        print('Set: confifTemp: ' + self.configTemp + '\n\n')

    def setConfigFilled(self, configFilled = ''):
        if configFilled != '':     # if supplied in function, set it
            self.configFilled = configFilled
        elif self.configFilled != '':  # if already set, do nothing
            return
        else:
            self.ConfigFilled = 'job.cfg'

    def setBindPaths(self, bindPaths = ''):
        if bindPaths != '':     # if supplied in function, set it
            self.binds = bindPaths
        print('Set: bindPaths: ' + self.binds + '\n\n')


    def runInsideContainerScript(self):
        f_runIn = open('run_nd280_insideContainer.sh', 'w')
        f_runIn.write('#!/bin/bash \n')
        f_runIn.write('export TMPDIR=${PWD} \n')
        f_runIn.write('export TEMP=${PWD} \n')
        f_runIn.write('export TMP=${PWD} \n')
        f_runIn.write('source /usr/local/t2k/current/nd280SoftwarePilot/nd280SoftwarePilot.profile \n')
        f_runIn.write('source /usr/local/t2k/current/nd280SoftwareMaster_*/bin/setup.sh \n')  
        f_runIn.write('export NeutronHPNames=YES  \n')  ## Deal with this somewhere better

        f_runIn.write('ENV_TSQL_URL="mysql://ccmyt2kro.in2p3.fr:3336/nd280calib;mysql://ccmyt2kro.in2p3.fr:3336/t2kbsd"\n')
        f_runIn.write('ENV_TSQL_USER="t2kcaldb_reader;t2kbsd_reader"\n')
        f_runIn.write('ENV_TSQL_PSWD="jY1JyaTq5uj2IdPo;jY1JyaTq5uj2IdPo"\n')

        self.setSetup()
        self.setRunCom()
        f_runIn.write(self.setup  + '\n')
        f_runIn.write('\n printenv \n\n' )
        f_runIn.write('\n cat *.cfg \n\n')
        f_runIn.write(self.runCom + '\n')
        f_runIn.write('exit_status=$? \n')
        f_runIn.write('echo "Finished, with exit status: $exit_status" \n\n')
        f_runIn.write('exit $exit_status\n')
        if(self.jobType == 'nd280sc_neutMC'):
            f_runIn.write('python3 check_nRooTracker.py \n' )
        f_runIn.close()

    def runOutsideContainerScript(self, gridfolder='', subsuffix='' ):

        bindPaths = ''
        if self.binds != '':
            bindPaths = self.binds
        f_runOut = open('run_nd280_outsideContainer.sh', 'w')
        #f_runOut.write('#!/bin/bash -x \n')
        f_runOut.write('#!/bin/bash \n')
        f_runOut.write('echo "True" > permissionToUpload.txt \n' )
        f_runOut.write('export IMAGE="'+ self.image +'" \n')
        f_runOut.write('singularity exec --cleanenv -B $PWD,/cvmfs/,' + bindPaths + ' $IMAGE ./run_nd280_insideContainer.sh 2>&1 | tee ' + self.jobFolder + '/nd280.log \n\n')
        f_runOut.write('exit_status=${PIPESTATUS[0]} \n')
        f_runOut.write('echo "Exit status of container executation of script:  $exit_status" \n')

        if gridfolder:
            f_runOut.write('if [ $exit_status -eq 0 ]; then \n')
            f_runOut.write('    echo "Uploading files..." \n')
            f_runOut.write('    python ./update_status.py   "Uploading files" \n')
            f_runOut.write('    python ./upload_search.py ' + gridfolder + '/' + subsuffix + ' 2>&1 | tee ' + self.jobFolder + '/upload.log \n')
            f_runOut.write('else \n')
            f_runOut.write('    echo "Exit status is non-zero, so I will not upload files to the grid" \n')
            f_runOut.write('fi \n') 

        f_runOut.write('ls -lh \n')
        f_runOut.close()
 
    def FillND280Config(self):
        
        # For purose of uploading.  Can remove this define cfg names.
        if self.jobType == 'nd280sc_neutSetup':
            os.system('cp job_temp.cfg neutSetup.cfg')
        elif self.jobType == 'nd280sc_neutMC':
            os.system('cp job_temp.cfg neutMC.cfg')
        elif self.jobType == 'nd280sc_nd280chain':
            os.system('cp job_temp.cfg ndn280chain.cfg')
           

        # Set up dictionary of strings to find and replace
        # d_nd280_findreplace['FIND'] = 'replace'
        d_nd280_findreplace = {}
        
        self.setConfigTemp()
        self.setConfigFilled()

        if (self.jobType == 'nd280sc_nd280chain' and self.runNum == '' and self.subrunNum == ''):
            print('Setting run and subrun based on filename')
            run = GetRunNumFromName(self.inputFile)
            subrun = GetSubrunNumFromName(self.inputFile)
            self.setRunSubrun(run, subrun) 

        run = self.runNum
        subrun = self.subrunNum
        
        print('FillND280Config - run = ' + str(run) )
        print('FillND280Config - subrun = ' + str(subrun) )

        inputfile = self.inputFile
        # If it is running on the grid, we assume the file was downloaded as part of the inputsandbox
        # and therefore strip the path, as the file should be in the working directory
        if inputfile.startswith('/t2k.org/'):
            inputfile = self.inputFile.split('/')
            inputfile = inputfile[-1]
           

        # nd280sc_neutMC
        d_nd280_findreplace['FILL_RUN'] = str(run)
        d_nd280_findreplace['FILL_SUBRUN'] = str(subrun)
        d_nd280_findreplace['FILL_NEUT_0_SEED'] = str(seedGenerator.GetRandomSeed(run,subrun,'numc0', hexbits=7))
        d_nd280_findreplace['FILL_NEUT_1_SEED'] = str(seedGenerator.GetRandomSeed(run,subrun,'numc1', hexbits=7))
        d_nd280_findreplace['FILL_NEUT_2_SEED'] = str(seedGenerator.GetRandomSeed(run,subrun,'numc2', hexbits=7))
        d_nd280_findreplace['FILL_NEUT_3_SEED'] = str(seedGenerator.GetRandomSeed(run,subrun,'numc3', hexbits=7))

        # nd280sc_nd280chain 
        d_nd280_findreplace['FILL_NUMCFILE'] = inputfile
        d_nd280_findreplace['FILL_G4SEED']  = str(seedGenerator.GetRandomSeed(str(run),str(subrun),'g4mc'))
        d_nd280_findreplace['FILL_ELECSEED'] = str(seedGenerator.GetRandomSeed(str(run),str(subrun),'elmc',hexbits=7))
        d_nd280_findreplace['FILL_NG4CI_1_SEED'] = str(seedGenerator.GetRandomSeed(str(run),str(subrun),'ng4ci_1',hexbits=7))
        d_nd280_findreplace['FILL_NG4CI_2_SEED'] = str(seedGenerator.GetRandomSeed(str(run),str(subrun),'ng4ci_2',hexbits=7))
        d_nd280_findreplace['FILL_NG4CI_3_SEED'] = str(seedGenerator.GetRandomSeed(str(run),str(subrun),'ng4ci_3',hexbits=7))
 
        # nd280sc_calib_ecal
        d_nd280_findreplace['FILL_MID'] = inputfile 

        com_copy_cfg = 'cp ' + self.configTemp + ' '+ self.configFilled
        print('com_copy_cfg: ' + com_copy_cfg)
        os.system( com_copy_cfg )
    
        f_temp = open( self.configTemp, 'r' )
    
        for i in d_nd280_findreplace:
            print(  i + '  :  ' +  'd_nd280_findreplace['+ i +'] = ' + d_nd280_findreplace[i]  )
            for line in fileinput.input(self.configFilled ,inplace=True):
                print( line.rstrip().replace(i, d_nd280_findreplace[i]) )
   
        os.system('echo ""; cat *.cfg; echo ""')
        return
        



def GetRunNumFromName(filename=''):
    # e.g. oa_nt_beam_90400128-0055_dddhhehiwqew_numc_000_magnet201011airrun4.root

    mod = filename.split('/')
    #print('mod = ', mod, '\n')
    mod0 = mod[-1].split('-')
    #print('mod0 = ' , mod0, '\n' )
    mod1 = mod0[0].split('_')
    #print('mod1 = ' , mod1, '\n' )    
    mod2 = mod1[-1:][0]
    #print('mod2 = ' , mod2, '\n' )  
    return mod2
    
    
def GetSubrunNumFromName(filename=''):
    # e.g. oa_nt_beam_90400128-0055_dddhhehiwqew_numc_000_magnet201011airrun4.root

    if('-' not in filename): 
       return '0'
    mod = filename.split('/')
    #print('mod = ', mod, '\n')
    mod0 = mod[-1].split('-')
    #print('mod0 = ' , mod0, '\n' )   
    mod1 = mod0[1].split('_')
    #print('mod1 = ' , mod1, '\n' )    
    mod2 = mod1[0]
    #print('mod2 = ' , mod2, '\n' )    
    return mod2
    

def GetRunNumFromNameEnd(filename='', zfill=3, precode=''):
    # Some sand neut vectors were named like this:
    # nu13a-nd13-fhc-2.5e17-94-9.root
    # -> This will return 94 (with zfill)
    # Midas files have _ between run and subrun instead of -
    # nd280_00010999_0040.daq.mid.g
    # -> This will return 00010999 with zfill

    mod = filename.rstrip('\n').split('/')
    #print(f"GetRunNumFromNameEnd: mod = {mod}\n")
    if '-' in mod:
        # This works for sand when '-' has been used
        mod0 = mod[-1].split('-')
    else:
        # This works for midas files which have '_'
        mod0 = mod[-1].split('_')
    #print(f"GetRunNumFromNameEnd: mod0 = {mod0}\n")
    mod1 = mod0[-2]
    #print(f"GetRunNumFromNameEnd: mod1 = {mod1}\n")    
    mod2 = precode + mod1.zfill(zfill)
    #print(f"GetRunNumFromNameEnd: mod2 = {mod2}\n")  
    return mod2
    
    
def GetSubrunNumFromNameEnd(filename='', zfill=4):
    # Some sand neut vectors were named like this:
    # nu13a-nd13-fhc-2.5e17-94-9.root
    # -> This will return 9 with zfill
    # Midas files have _ between run and subrun instead of -
    # nd280_00010999_0040.daq.mid.g
    # -> This will return 0040 with zfill

    mod0 = re.split('[-_]', filename)
    #print(f"mGetSubrunNumFromNameEnd: mod0 = {mod0} \n")   
    mod1 = mod0[-1].rstrip('\n').rstrip('.root').rstrip('.kin').rstrip('.daq.mid.gz')
    #print(f"mGetSubrunNumFromNameEnd: mod1 = {mod1} \n")    
    mod2 = mod1.zfill(zfill)
    #print(f"mGetSubrunNumFromNameEnd: mod2 = {mod2} \n")    
    return mod2
    
           
