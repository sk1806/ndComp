#!/usr/bin/env python

# Script to register a list local files in the hyperk.org DFC
# soph.e.king123@gmail.com


#  Relevant documentation
#https://dirac.readthedocs.io/en/stable/CodeDocumentation/DataManagementSystem/Client/DataManager.html
#https://dirac.readthedocs.io/en/stable/DeveloperGuide/AddingNewComponents/DevelopingCommands/index.html#coding-commands


#  Relevant functions
#
# DataManager module
#  def getReplicaIsFile( self, lfn, storageElementName, singleFile = False ):
#    """ Determine whether the supplied lfns are files at the supplied StorageElement
#
#        'lfn' is the file(s) to check
#        'storageElementName' is the target Storage Element  """

#import os
#import sys
#sys.path.append('../../libFns')

from diracTools import dirac__ls

from DIRAC.Core.Base import Script
Script.parseCommandLine() 

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
dm = DataManager()







#clean     = 'p6T_run5water_anti-neut_D' # local subfolder folder
#dfc_path  = "/t2k.org/nd280/production00X/A/mcp/anti-neut_B/YYYY-YY-water/magnet/runZ/"  #DFN
#type_dir  = "numc"
#lower_lim = 999 
#type_dir = "anal"
#lower_lim = 999


# e.g.
#clean     = 'p6T_run5water_anti-neut_D'
#dfc_path  = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2010-11-water/magnet/run5/"
##type_dir  = "numc"
##lower_lim = 1900000 
#type_dir = "anal"
#lower_lim = 75000000





#clean = 'p6T_run9water_x_anti-neut_D'
#dfc_path = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2015-08-water/magnet/run9x/"
#type_dir = "numc"
#lower_lim = 1900000
#type_dir = "anal"
#lower_lim = 75000000 




#clean = 'p6U_run4air_neut_D'
#dfc_path = '/t2k.org/nd280/production006/U/mcp/neut_D/2010-11-air/magnet/run4/'
#type_dir = "numc"
#lower_lim = 56000000 
#type_dir = "anal"
#lower_lim = 200000000




### P6T ###
lower_lim_p6t_anal_rhc = 75000000
lower_lim_p6T_numc_rhc = 1900000 

## RHC

#clean     = 'p6T_run5water_anti-neut_D'
#dfc_path  = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2010-11-water/magnet/run5/"
#type_dir  = "numc"
#lower_lim = 1900000 
##type_dir = "anal"
##lower_lim = lower_lim_p6t_anal_rhc

#clean = 'p6T_run6air_anti-neut_D'
#dfc_path = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2010-11-air/magnet/run6/"
#type_dir = "numc"
#lower_lim = lower_lim_p6T_numc_rhc 
#type_dir = "anal"
#lower_lim = lower_lim_p6t_anal_rhc

#clean = 'p6T_run7water_anti-neut_D'
#dfc_path = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2015-08-water/magnet/run7/"
##type_dir = "numc"
##lower_lim = lower_lim_p6T_numc_rhc
#type_dir = "anal"
#lower_lim = lower_lim_p6t_anal_rhc

#clean = 'p6T_run9water_anti-neut_D'
#dfc_path = "/t2k.org/nd280/production006/T/mcp/anti-neut_D/2015-08-water/magnet/run9/"
##type_dir = "numc"
##lower_lim = lower_lim_p6T_numc_rhc 
#type_dir = "anal"
#lower_lim = lower_lim_p6t_anal_rhc


## FHC

#clean = 'p6T_run2air_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2010-11-air/magnet/run2/'
##type_dir = "numc"
##lower_lim = 56000000 
#type_dir = "anal"
#lower_lim = 200000000 

#clean = 'p6T_run2water_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2010-11-water/magnet/run2/'
#type_dir = "numc"
#lower_lim = 56000000
#type_dir = "anal"
#lower_lim = 200000000

# p6T run3air neutD
#clean = 'p6T_run3air_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2010-11-air/magnet/run3/'
##type_dir = "numc"
##lower_lim = 56000000 
#type_dir = "anal"
#lower_lim = 200000000

#clean = 'p6T_run4air_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2010-11-air/magnet/run4/'
#type_dir = "numc"
#lower_lim = 56000000 
#type_dir = "anal"
#lower_lim = 200000000

#clean = 'p6T_run4water_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2010-11-water/magnet/run4/'
#type_dir = "numc"
#lower_lim = 56000000
#type_dir = "anal"
#lower_lim = 200000000

#clean = 'p6T_run8air_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2015-08-air/magnet/run8/'
#type_dir = "numc"
#lower_lim = 56000000
#type_dir = "anal"
#lower_lim = 192000000

#clean = 'p6T_run8water_neut_D'
#dfc_path = '/t2k.org/nd280/production006/T/mcp/neut_D/2015-08-water/magnet/run8/'
##type_dir = "numc"
##lower_lim = 56000000
#type_dir = "anal"
#lower_lim = 192000000

#clean = 'p7_v02_run4air_neut_D'
dfc_path = '/t2k.org/nd280/production007/validation/V03/mcp/neut_D/2010-11-air/magnet/run4/'
#type_dir = "numc"
#lower_lim = 56000000 
type_dir = "anal"
lower_lim = 200000000

clean = 'p7_v04_run4air_neut_D'
dfc_path = '/t2k.org/nd280/production007/validation/V04/mcp/neut_D/2010-11-air/magnet/run4/'
type_dir = "numc"
lower_lim = 56000000 
#type_dir = "anal"
#lower_lim = 200000000



local_path = '/mnt/lustre/groups/nms_epapg/k1919811/qm/king/grid/prodTools/t2k/t2k_cleanProd/' + clean


fullList  = local_path+'/size_'+type_dir+'_full.list'
smallList = local_path+'/size_'+type_dir+'_small.list'
delList   = local_path+'/size_'+type_dir+'_del.list'
errorList = local_path+'/size_'+type_dir+'_error.list'
erresList = local_path+'/size_'+type_dir+'_erres.list'
delList   = local_path+'/size_'+type_dir+'_del.size'
errorList = local_path+'/size_'+type_dir+'_error.size'
erresList = local_path+'/size_'+type_dir+'_erres.size'

f_size_full  = open(fullList, "w+")
f_size_small = open(smallList,"w+")
f_size_del   = open(delList,  "w+")
f_size_error = open(errorList,"w+")
f_size_erres  = open(erresList, "w+")



#dfc_list = dirac__ls(dfc_path + type_dir)
dfc_list = list_dir((dfc_path + type_dir))

site = ["CA-SFU-T21-disk", "UKI-LT2-QMUL2-disk", "UKI-LT2-IC-HEP-disk", "IN2P3-CC-T2K-disk", "UKI-SOUTHGRID-RALPP-disk"] 



for lfn in dfc_list:



    foundSite = False
    siteCount = 0
    print('')
    print('')
    print('')
    print('')
    print(lfn)
    print('')

    while(foundSite == False):

        print('')
        print('')
        print('Checking site' ),
        print(site[siteCount])
        # try to obtain size
        res = dm.getReplicaSize(lfn, site[siteCount])
        print('done initial res')
        print(res)
        print('printed res')
        print('')
        print('about to try get fail')
        try:
            fail = res['Value']['Failed']
            print('collected fail and about to print...')
            print(fail)
            if(fail == {} ):
                print('No Fail {}')
                foundSite = True
                print(' Found site : ' + site[siteCount])
                print('')
                continue
            else:
                print('Failed')
                print('')
                print('about to collect fail_lfn')
                fail_lfn = res['Value']['Failed'][lfn]
                print('collected fail_lfn and abou to print it...')
                print(fail_lfn)
                print('printed fail lfn')
                if(fail_lfn == ''):
                    print('Not failed lfn {}')
                else:
                    print('Failed lfn')

                if(fail_lfn == "File hasn't got replica at supplied Storage Element."):
                    siteCount = siteCount +1
                else:
                    continue
        except:
            print('Error for:  '),
            print(lfn)
            str_lfn = lfn + '\n'
            f_size_error.write(str_lfn)
            str_error_site = site[siteCount] + '\n'
            str_error_res = str(res) + '\n'
            f_size_erres.write(str_lfn)
            f_size_erres.write(str_error_site)
            f_size_erres.write(str_error_res)
            f_size_erres.write('\n')





    res = dm.getReplicaSize(lfn, site[siteCount])




    print('')
    print('')
    print('Found site, about to check size')
    print('')
    print(lfn)
    try:
        size = res['Value']['Successful'][lfn]
        str_lfn = lfn + '\n'
        str_size_lfn = str(size) + " : " + str_lfn
        print(str_size_lfn)
        f_size_full.write(str_size_lfn)
        print('Checking size')
        if(size < lower_lim):
            f_size_small.write(str_size_lfn)
            f_size_del.write(str_lfn)
    except:
        print('Error for:  '),
        print(lfn)
        str_lfn = lfn + '\n'
        f_size_error.write(str_lfn)
        str_error_site = site[siteCount] + '\n'
        str_error_res = res['Value']['Failed'][lfn] + '\n'
        f_size_erres.write(str_lfn)
        f_size_erres.write(str_error_site)
        f_size_erres.write(str_error_res)
        f_size_erres.write('\n')
    


       
    
f_size_full.close()
f_size_small.close()      
f_size_del.close()
f_size_error.close()
f_size_erres.close()

