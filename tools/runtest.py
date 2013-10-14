#!/usr/bin/env python

import sys
import os
import csv
import subprocess

def runHB(row, font, positions=False):
    args = ["hb-shape", "--no-clusters", positions and "--debug" or "--no-positions",
            "--font-file=%s" %font,
            "--direction=%s" %row[0],
            "--script=%s"    %row[1],
            "--language=%s"  %row[2],
            "--features=%s"  %row[3],
            "--text=%s"      %row[4]]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    return process.communicate()[0].strip()

def runTest(test, font, positions):
    count = 0
    failed = {}
    passed = []
    for row in test:
        count += 1
        row[4] = ('\\' in row[4]) and row[4].decode('unicode-escape') or row[4]
        text = row[4]
        reference = row[5]
        result = runHB(row, font, positions)
        if reference == result:
            passed.append(count)
        else:
            failed[count] = (text, reference, result)

    return passed, failed

def initTest(test, font, positions):
    out = ""
    for row in test:
        text = row[4]
        row[4] = ('\\' in row[4]) and row[4].decode('unicode-escape') or row[4]
        result = runHB(row, font, positions)
        out += "%s;%s;%s\n" %(";".join(row[:4]), text, result)

    return out

if __name__ == '__main__':
    init = False
    positions = False
    args = sys.argv[1:]

    if len (sys.argv) > 2 and sys.argv[1] == "-i":
        init = True
        args = sys.argv[2:]

    for arg in args:
        testname = arg

        ext = os.path.splitext(testname)[1]
        if ext == '.ptest':
            positions = True

        reader = csv.reader(open(testname), delimiter=';')

        test = []
        for row in reader:
            test.append(row)

        if init:
            fontname = 'amiri-regular.ttf'
            outname = testname+".test"
            outfd = open(outname, "w")
            outfd.write(initTest(test, fontname, positions))
            outfd.close()
            sys.exit(0)

        if positions:
            styles = ('regular', )
        else:
            styles = ('regular', 'bold', 'slanted', 'boldslanted')

        for style in styles:
            fontname = 'amiri-%s.ttf' % style
            passed, failed = runTest(test, fontname, positions)
            message = "%s: font '%s', %d passed, %d failed" %(os.path.basename(testname),
                    fontname, len(passed), len(failed))

            print message
            if failed:
                for test in failed:
                    print test
                    print "string:   \t", failed[test][0]
                    print "reference:\t", failed[test][1]
                    print "result:   \t", failed[test][2]
                sys.exit(1)
