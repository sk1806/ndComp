#!/usr/bin/env python3

import os
import sys
import fileinput
import optparse

sys.path.append('./fromND280Computing')
from ND280GRID import GetRandomSeed



run = '80710119'
subrun = '0055'

g4mc_seed = str(GetRandomSeed(str(run),str(subrun),'g4mc'))
elmc_seed = str(GetRandomSeed(str(run),str(subrun),'elmc',hexbits=7))
g4ci_seed = str(GetRandomSeed(str(run),str(subrun),'ng4ci_1',hexbits=7))

print(g4mc_seed)
print(elmc_seed)
print(g4ci_seed)

