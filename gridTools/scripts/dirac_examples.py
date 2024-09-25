#!/usr/bin/env python3

from datetime import datetime

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
dm = DataManager()




str_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
local_file = f"test_{str_datetime}.txt"

with open(local_file, "w") as f:
    f.write("aghh")

grid_file = f"/t2k.org/user/k/sophie.king/{local_file}"


#putAndRegister(lfn, fileName, diracSE, guid=None, path=None, checksum=None, overwrite=False)
res_upload = dm.putAndRegister( grid_file, local_file, 'IN2P3-CC-XRD-disk' ) 
print(res_upload)
print('')


#getActiveReplicas(lfns, getUrl=True, diskOnly=False, preferDisk=False, protocol=None)
res_get_reps = dm.getActiveReplicas(grid_file, True, False)
print(res_get_reps)
print('')

#replicateAndRegister(lfn, destSE, sourceSE='', destPath='', localCache='', catalog='')
res_replicate = dm.replicateAndRegister(grid_file, 'IN2P3-CC-XRD-disk',  'UKI-LT2-IC-HEP-disk')
print(res_replicate)
print('')
