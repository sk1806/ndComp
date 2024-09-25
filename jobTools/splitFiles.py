#!/usr/bin/env python 


# for i in range (0,100,1):
#     x=str(i).zfill(4)
#     print(x)
# exit()


import fileinput
import os

sign = 'pos'
#sign = 'neg'

start = 40
end = 60

#for i in range(start,end,1):
#    name = 'vector_'+sign+'_1e22_HK_Tochibora_LBL2019Mar'
#
#    inFile = sign+'/'+name + '_'+  str(i).zfill(4) +'.dat'    
#    command_ls = 'ls ' + inFile
#    os.system(command_ls)
#
#    rootFile = sign+'/'+name + '_'+  str(i).zfill(4) +'.root'    
#    command_ls = 'ls ' + rootFile
#    os.system(command_ls)
#
#exit()



for i in range(start,end,1):


    countEvents = 0
    countFiles = 0

    name = 'vector_'+sign+'_1e22_HK_Tochibora_LBL2019Mar'
    inFile = sign+'/'+name + '_'+  str(i).zfill(4) +'.dat'    
    print('Splitting:  ' + inFile)

    # sort the split files into sub folders
    # could easily make this less hard coded
    folders = []
    folders.append('./'+sign+'_split_dat/0000_0000-0019_9999')
    folders.append('./'+sign+'_split_dat/0020_0000-0039_9999')
    folders.append('./'+sign+'_split_dat/0040_0000-0059_9999')
    folders.append('./'+sign+'_split_dat/0060_0000-0079_9999')
    folders.append('./'+sign+'_split_dat/0080_0000-0099_9999')

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    if(  i>=0  and i<20): pre = folders[0] 
    elif(i>=20 and i<40): pre = folders[1] 
    elif(i>=40 and i<60): pre = folders[2] 
    elif(i>=60 and i<80): pre = folders[3] 
    elif(i>=80 and i<1000): pre = folders[4] 


    search = open(inFile)
    for line in search:


        if 'begin' in line:

            if( countFiles ==0 and countEvents==0):
                outFile = pre+'/'+name+'_'+ str(i).zfill(4)  +'_' + str(countFiles).zfill(4) + '.dat'
                f = open(outFile, "a+")
     
            if(countEvents == 30):
                f.close()
                countFiles += 1
                outFile = pre+'/'+name+'_'+ str(i).zfill(4)  +'_' + str(countFiles).zfill(4) + '.dat'
                f = open(outFile, "a+")
                countEvents = 0

            countEvents += 1
            f.write(line)
            print(outFile)
        else: 
            f.write(line)
               
                                              
