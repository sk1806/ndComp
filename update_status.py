### update_status.py ###
#!/usr/bin/env python
import os
import sys

from DIRAC.Core.Base import Script
Script.initialize()
from DIRAC.WorkloadManagementSystem.Client.JobReport import JobReport

jobid = os.getenv('DIRACJOBID')
if not jobid:
  print("This command only works from within a DIRAC job")
  sys.exit(1)
if len(sys.argv) < 2:
  print("Usage: update_status.py <status message>")
  sys.exit(1)
appstatus = sys.argv[1]

jr = JobReport(int(jobid))
res = jr.setApplicationStatus(appstatus)
if not res['OK']:
  print("Failed to update application status: %s" % str(res))
  sys.exit(1)
sys.exit(0)
