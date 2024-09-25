#!/usr/bin/env python

import os
import sys
import optparse
import time
from datetime import datetime


from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
dm = DataManager()

from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

#https://dirac.readthedocs.io/en/stable/CodeDocumentation/DataManagementSystem/Client/DataManager.html
#https://dirac.readthedocs.io/en/stable/DeveloperGuide/AddingNewComponents/DevelopingCommands/index.html#coding-commands

# DataManager module
  # putAndRegister(lfn, fileName, diracSE, guid=None, path=None, checksum=None, overwrite=False)
  #  e.g.  print dm.putAndRegister('/t2k.org/user/king/test_api_DFCname.txt', './test_api.txt', 'UKI-LT2-QMUL2-disk')



def is_file(filename):

    fc = FileCatalog()
    res = fc.isFile(filename)
    print(res)
    print("res['Value']['Successful']['",filename,"'] =      ", res['Value']['Successful'][filename])
    is_it = res['Value']['Successful'][filename]
    return is_it


#def list_dir(path, out_file):
#
#    fc = FileCatalog()
#    res = fc.listDirectory(path)
#    if not res['OK']:
#        message = f"Failed to list path '{path}': {res['Message']}"
#        print(message) 
#        print(message, file=sys.stderr)  
#        return
#    listing = res['Value']['Successful'][path]
#
#    f_out = open(out_file, "w")
#    for item in sorted(listing['Files'].keys() + listing['SubDirs'].keys()):
#        f_out.write(item + '\n')


def list_dir(path, out_file = ''):

    fc = FileCatalog()
    res = fc.listDirectory(path)
    if not res['OK']:
        message = f"Failed to list path '{path}': {res['Message']}"
        print(message)         
        print(message, file=sys.stderr)
        return
    listing = res['Value']['Successful'][path]

    if out_file != '':
        f_out = open(out_file, "w")
    files = []
    for item in sorted(list(listing['Files'].keys()) + list(listing['SubDirs'].keys())):

        if out_file != '':
            f_out.write(item + '\n')
        files.append(item)
    return files




#def dirac__ls(path):
#  """List files (non-recursively) in a directory
#     path should take the form  '/vo/path/to/list 
#     e.g.  /t2k.org/user """
#
#  fc = FileCatalog()
#  res = fc.listDirectory(path)
#  if not res['OK']:
#    print >>sys.stderr, "Failed to list path '%s': %s", path, res['Message']
#    return
#  listing = res['Value']['Successful'][path]
#  files=[]
#  for item in sorted(listing['Files'].keys() + listing['SubDirs'].keys()):
#    #print(item)
#    files.append(item)
#  #print(files)
#  return files
                               




def upload(LFN='', LOCAL='', SE='CA-SFU-T21-disk'):
    """usage: uploads LOCAL file to storage element SE, under the path/name LFN 
       returns:  0 - uploaded,   1 - file already existed,  2 - upload failed
    """
    # TODO - Maybe add an option for overwriting if the file already exists
    print('')
    print(datetime.now())
    print(f'Consider upload:  {LFN}  {LOCAL} {SE}')

    if is_file(LFN):
        print(f'- File {LFN} already exists. NOT attempting to upload.')
        return 1

    print('- Checked file does not exist, now attempting upload')
    for count in range(10):
        print(f'Upload attempt {count}')
        upload_result = dm.putAndRegister(LFN, LOCAL, SE)
        print(f'\n{upload_result}\n')
        print(datetime.now())

        if upload_result['OK']:
            return 0
        # On the final attempt, run the command line function with -ddd
        # Because this prints more useful debug info to the log
        if count == 9:
            com_upload = f'dirac-dms-add-file -ddd {LFN} {LOCAL} {SE}'
            print(com_upload)
            final_result = os.system(com_upload)
            if final_result == 0:
                return 0

    return 2

