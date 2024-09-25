#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import isfile, join
import argparse

import gridTools
import fileTools

# This puts files into an upload list
def main():
    
    parser = argparse.ArgumentParser(description='Upload Search Script')
    parser.add_argument('gridfolder', help='The LFN folder (mandatory)')
    parser.add_argument('subsuffix', nargs='?', default='', help='The suffix to add to subfolder, e.g., "ecalmod" for cali_ecalmod')

    args = parser.parse_args()

    gridpath = args.gridfolder
    subsuffix = args.subsuffix

    print(f'Grid path: {gridpath}')
    print(f'Subsuffix: {subsuffix}')

    # for nd280sc_neutMC jobs, check_nRooTracker.py is run inside the nd280 container
    # If the nRooTracker TTree does not exist, it will replace 'True' with 'False' in permissionToUpload.txt
    # Not pretty, but we have access to uproot inside nd280Container but not the dirac environment outside it
    print('\nChecking if I have permission to upload...')
    f_permissions = open('permissionToUpload.txt', 'r')
    try:
        with open('permissionToUpload.txt', 'r') as file:
            contents = file.read().strip()
            print(contents)
    
            if contents != 'True':
                os.sys.exit("I do not have permission to upload.")
    except FileNotFoundError:
        os.sys.exit("I cannot find permissionToUpload.txt, so I will not upload.")
    print("I have persmission to upload.")
    
    # tar the catalogue files
    fileTools.create_tarball_suffix('./', '_catalogue.dat', True, '')

    mypath = './'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
   
    SE = 'IN2P3-CC-XRD-disk'    
 
    f_upload = open('upload_search.list' , 'w+')
    
    b_allOK = True
    files = listdir(mypath)
    print('\n Files in dir: \n')
    print(files)
    print('')

    for f in files:
        print(f'\n\nFile:  {f}')
        if isfile(join(mypath, f)):  # check this is a file (not directory)
    
            b_upload = False
            # TODO - automate this based on job type, with optional override 
            # Hardcoding this here is yuck.
            if '_numc_' in f and '.root' in f and '.geo.root' not in f:                   
                TYPE = 'numc'
                b_upload = True
            elif '_evtr' in f and '.root' in f:
                TYPE = 'evtr'
                b_upload = True
            elif '_cata' in f and '.tar.gz' in f:
                TYPE = 'cata'
                b_upload = True
            elif '_logn_' in f and '.log' in f:
                TYPE = 'logn'
                b_upload = True
            elif '_g4mc_' in f and '.root' in f:
                TYPE = 'g4mc'
                b_upload = True
            elif '_elmc_' in f and '.root' in f:
                TYPE = 'elmc'
                b_upload = True
            elif '_cali_' in f and '.root' in f:
                TYPE = 'cali'
                b_upload = True
            elif '_reco_' in f and '.root' in f:
                TYPE = 'reco'
                b_upload = True
            elif '_anal_' in f and '.root' in f:
                TYPE = 'anal'
                b_upload = True
            elif '_logf_' in f and '.log' in f:
                TYPE = 'logf'
                b_upload = True
            elif '.cfg' in f:
                TYPE = 'cnfg'
                b_upload = True    
            elif ('.DAT' in f or '.dat' in f):
                TYPE = 'dat'
                b_upload = True    
                if 'catalogue' in f:
                    b_upload = False
            elif ('_stft_' in f and 'root' in f):
                TYPE = 'stft'
                b_upload = True
            elif ('_cmud_' in f and 'root' in f):
                TYPE = 'cmud'
                b_upload = True
            elif '.tar.gz'in f and 'oa_' in f:
                TYPE = 'cata'
                b_upload = True

            if b_upload:
                if subsuffix:
                    TYPE = TYPE + '_' + subsuffix
            
                LFN = gridpath.rstrip('/') + '/' + TYPE + '/' + f
                print(LFN)
                f_upload.write(LFN + ' \n')
            
                b_uploaded = gridTools.upload(LFN, f, SE)
                print(f'Upload return code:, {b_uploaded} (0 - OK,  1 - Already exists,  2 - Failed)')
                if b_uploaded == 2:
                    b_allOK = False
                    print('Upload failed:', LFN)
                    break


    f_upload.close()
    if b_allOK == False:
        print('Upload of a file failed... cleaning all files')
        com_del = 'dirac-dms-remove-files upload_search.list'
        clean = os.system(com_del)
        if clean == 0:
            print('Clean complete')
        else: 
            print('Clean failed')

main()
