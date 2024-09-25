#!/usr/bin/env python3 


import fileinput
import argparse

def splitFiles( inFile , outFilePrefix , outFileZfill = 4, outFileSuffix = '.kin', splitBefore = '$ begin', nPerFile = 100, startAt = 0, stopAfter = 10000000000000):
    """Splits txt files into multiple files based on a given string separator.

        splitFiles( inFile = '', outFilePrefix = '', outFileZfill = 4, outFileSuffix = '.kin', splitBefore = '$ begin', nPerFile = 100, startAt = 0, stopAfter = 1000000000 )

        inFile - input txt file that you want to split

        outFileZfill = 4 and outFileSuffix = '.kin'
        output:  outFilePrefix_####.kin

        e.g. for splitting kin files, then splitBefore = 'Begin'
             And if you want 100 events, nPerFile = 100 (0-99)

        startAt = 11 --> starts at event #10 numbered from 0
        stopAafter  = 3000 --> writes out 0 - 2999 events then stops (where 0 is the event it starts at)
    """


    f_in = open(inFile, "r")
    lines = f_in.read()
    nEvents = lines.count(splitBefore)
    print(inFile + ' contains ' + str(nEvents) + ' events')
    
    f_in.seek(0)  # Reset the file pointer to the beginning of the file

    countLine = 0
    countEvents = 0
    countEventsInThisFile = 0
    countFiles = 0
    maxFiles = int( int(outFileZfill) * '9' )

    for line in f_in:
        countLine += 1
        #print('countLine 1 - ' + str(countLine) )
        #print(' -- ' + line)
        if countEvents < int(startAt):  continue
        if countFiles > maxFiles:
            print('You have reached the maximum number of files that can be accomodated with this zfill setting, ' + str(maxFiles) + ', but have not finished the splitting') 
            return 1
        if( countEventsInThisFile == 0 and countFiles == 0):
           outFile = outFilePrefix + str(countFiles).zfill(int(outFileZfill)) + outFileSuffix
           f_out = open(outFile, "w")
           countFiles +=1

        if splitBefore in line:
            if( countEvents == int(stopAfter) ): 
                print('Not adding this line, we have reached the maximum number of occurances')
                return 0
            if(countEventsInThisFile == int(nPerFile) ):
                f_out.close()
                outFile = outFilePrefix + str(countFiles).zfill(int(outFileZfill)) + outFileSuffix
                f_out = open(outFile, "w")
                f_out.write(line)
                #print('Added to ' + outFile)
                countFiles += 1
                countEventsInThisFile = 1
                #print('countEventsInThisFile: 1 -', countEventsInThisFile)
                #print('countFiles:  1 -', countFiles)
            else:
                countEventsInThisFile += 1
                f_out.write(line)
                #print('Added to ' + outFile)
            countEvents += 1
            #print('countEvents: 1 -', countEvents)

        else:
            f_out.write(line)
            #print('Added to ' + outFile)
        #print('countEvents: 1 -', countEvents)
        #print('countEventsInThisFile: 1 -', countEventsInThisFile)
        #print('countFiles:  1 -', countFiles)
    print('End of file')    
    return 1


def splitFilesRunSubrun( inFile , outFilePrefix , outFileZfill = 8, subrunPerRun = 56, subrunZfill = 4,  outFileSuffix = '.kin', splitBefore = '$ begin', nPerFile = 100, startAt = 0, stopAfter = 10000000000000 ):

    f_in = open(inFile, 'r')
    lines = f_in.read()
    nEvents = lines.count(splitBefore)
    print(inFile + ' contains ' + str(nEvents) + ' events')
    
    f_in.seek(0)  # Reset the file pointer to the beginning of the file

    nPerRun = int(nPerFile) * int(subrunPerRun)
    stopAfter = nPerRun

    run = 0
    result = 0
    print('stopAfter ' + str(stopAfter) )
    print('nEvents ' + str(nEvents) )

    while (result == 0 ) :
        print('run = ' + str(run))
        result = splitFiles( inFile , outFilePrefix + '_' + str(run).zfill(int(outFileZfill)) + '-' , subrunZfill, outFileSuffix, splitBefore, nPerFile, startAt, stopAfter )
        print('result = ' + str(result))
        run += 1



if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog = "Splits txt files into multiple files based on a given string separator.")
    #description=("splitFiles( inFile = '', outFilePrefix = inFile.split('.')[0]+'_', outFileZfill = 4, outFileSuffix = '.kin', splitBefore = '$ begin', nPerFile = 100, startAt = 0, stopAfter = 1000000000 )"))

    parser.add_argument('-i', '--infile', dest='inFile', action='store', required=True,
                    help='Input file to split')

    parser.add_argument('-p', '--prefix', dest='outFilePrefix', action='store', required=False,
                    help='Prefix to the output file names')

    parser.add_argument('-z', '--zfill', dest='outFileZfill', action='store', required=False,
                    help='zfill for the output file names (number of digits in output file names)')

    parser.add_argument('-s', '--suffix', dest='outFileSuffix', action='store', required=False,
                    help='Suffix for the out file names')

    parser.add_argument('-c', '--split', dest='splitBefore', action='store', required=False,
                    help='Cut just before this string.  This is the string that signifies the start of the next thing')

    parser.add_argument('-n', '--nperfile', dest='nPerFile', action='store', required=False,
                    help='Number of occurances to be put in each file (count from 1)')

    parser.add_argument('-b', '--startat', dest='startAt', action='store', required=False,
                    help='Begin at the # occurance (count from 1)')

    parser.add_argument('-e', '--stopat', dest='stopAfter', action='store', required=False,
                    help='End after # occurances (count from 1)')

    parser.add_argument( '--subrunperrun', dest='subrunPerRun', action='store', required=False,
                    help='Number of subruns per run in outputfile naming.  Supply this if you want a run-subrun naming convention.')

    parser.add_argument('--subrunzfill', dest='subrunZfill', action='store', required=False,
                    help='zfill the subrun to this many digits.  Supply this if you want a run-subrun naming convention')

   

    args = parser.parse_args()
        

    inFile = args.inFile

    if(args.outFilePrefix is not None): outFilePrefix = args.outFilePrefix
    else:
        if(args.subrunPerRun is not None and args.subrunZfill is not None): 
            outFilePrefix = inFile.split('.')[0]
        else:
            outFilePrefix = inFile.split('.')[0]+'_'

    if(args.outFileZfill is not None): outFileZfill = args.outFileZfill
    else:  outFileZfill = 4

    if(args.outFileSuffix is not None): outFileSuffix = args.outFileSuffix
    else:  outFileSuffix = '.kin'

    if(args.splitBefore is not None): splitBefore = args.splitBefore
    else: splitBefore = '$ begin' 

    if(args.nPerFile is not None): nPerFile = args.nPerFile
    else: nPerFile = 100

    if(args.startAt is not None): startAt = args.startAt
    else: startAt = 0

    if(args.stopAfter is not None): stopAfter = args.stopAfter
    else: stopAfter = 10000000000000

    subrunPerRun = args.subrunPerRun
    subrunZfill= args.subrunZfill


    if(subrunPerRun is not None or subrunZfill is not None):
        if(subrunPerRun is not None and subrunZfill is not None):
            splitFilesRunSubrun( inFile , outFilePrefix, outFileZfill, subrunPerRun,  subrunZfill, outFileSuffix, splitBefore, nPerFile, startAt, stopAfter)
        else:
            print("You must supply subrunPerRun AND runZfill, you can't supply just one")
    else:
        splitFiles( inFile , outFilePrefix, outFileZfill, outFileSuffix, splitBefore, nPerFile, startAt, stopAfter)
   



