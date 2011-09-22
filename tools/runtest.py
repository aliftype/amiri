#!/usr/bin/python

import sys
import os
import csv
import subprocess

def runHB(row, font):
    args = ["hb-shape", "--no-clusters", "--no-positions",
            "--font-file=%s" %font,
            "--direction=%s" %row[0],
            "--script=%s"    %row[1],
            "--language=%s"  %row[2],
            "--features=%s"  %row[3],
            "--text=%s"      %row[4]]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    return process.communicate()[0].strip()

def runTest(reader, font):
    count = 0
    failed = {}
    passed = []
    for row in reader:
        count += 1
        text = row[4]
        reference = row[5]
        result = runHB(row, font)
        if reference == result:
            passed.append(count)
        else:
            failed[count] = (text, reference, result)

    return passed, failed

def initTest(reader, font):
    out = ""
    for row in reader:
        result = runHB(row, font)
        out += "%s;%s\n" %(";".join(row), result)

    return out

if __name__ == '__main__':
    init = False
    args = sys.argv[1:]

    if len (sys.argv) > 2 and sys.argv[1] == "-i":
        init = True
        args = sys.argv[2:]

    for arg in args:
        testname = arg

        testfd = open(testname, 'r')
        fontname = testfd.readline().strip("# \n")
        reader = csv.reader(testfd, delimiter=';', quotechar='#')

        if init:
            outname = testname+".test"
            outfd = open(outname, "w")
            outfd.write(initTest(reader, fontname))
            outfd.close()
            sys.exit(0)

        passed, failed = runTest(reader, fontname)
        message = "%s: %d passed, %d failed" %(os.path.basename(testname), len(passed), len(failed))

        if failed:
            print message
            for test in failed:
                print test
                print "string:   \t", failed[test][0]
                print "reference:\t", failed[test][1]
                print "result:   \t", failed[test][2]
            sys.exit(1)
        else:
            print message
