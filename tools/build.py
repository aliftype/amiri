#!/usr/bin/python
import fontforge
import os
import sys


family = "amiri"
styles = ("math", "regular", "bold", "italic", "bolditalic")
flags  = ("opentype",)
source = "sources"
args   = [ ]

if len(sys.argv) > 1:
    args = list(sys.argv[1:])

for arg in args:
    if arg == "all":
        args = styles
    elif not arg in styles:
        print "Unkown style requested: %s" %arg
        args.remove(arg)

if len(args) == 0:
    args = styles

for style in args:
    name = family+"-"+style
    if os.path.isfile(os.path.join(source, name+".sfd")):
        print "Generating %s..." % style
        font = fontforge.open(os.path.join(source, name+".sfd"))
        font . generate(name+".ttf", flags=flags)
        font . close()
