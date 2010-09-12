#!/usr/bin/python
import fontforge
import os
import sys

family = "amiri"
source = "sources"
flags  = ("opentype", "dummy-dsig", "round", "short-post")

def main(style):
    style = style.lower()
    base = os.path.join(source, "%s-%s" %(family, style))
    if os.path.isfile("%s.sfd" % base):
        file = "%s.sfd" % base
    elif os.path.isdir("%s.sfdir" % base):
        file = "%s.sfdir" % base
    else:
        print "Font for style: '%s' not found" % style
        sys.exit(1)

    font = fontforge.open(file)

    print "Gnerating %s-%s.ttf" %(family, style)
    font.generate("%s-%s.ttf" %(family, style), flags=flags)

    font.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "No style specified"
        sys.exit(1)
