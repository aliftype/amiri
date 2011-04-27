#!/usr/bin/python
#
# build.py - Amiri font build utility
#
# Written in 2010-2011 by Khaled Hosny <khaledhosny@eglug.org>
#
# To the extent possible under law, the author have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import fontforge
import sys
import os
import getopt
import tempfile

def genCSS(font, base):
    if font.fullname.lower().find("slanted")>0:
        style = "slanted"
    else:
        style = "normal"

    weight = font.os2_weight
    family = "%sWeb" %font.familyname
    name = font.fontname

    css = """
@font-face {
    font-style: %(style)s;
    font-weight: %(weight)s;
    font-family: %(family)s;
    src: url('%(base)s.eot?') format('eot'),
         url('%(base)s.woff') format('woff'),
         url('%(base)s.ttf')  format('truetype');
}
""" %{"style":style, "weight":weight, "family":family, "base":base}

    return css

def genClasses(font, klasses):
    text = ""
    for klass in klasses.split():
        text += "@%s = [" %klass.title()

        for glyph in font.glyphs():
            if glyph.glyphclass == klass:
                text += glyph.glyphname + " "

        text += "];\n"

    return text

def usage(code):
    message = """Usage: %s OPTIONS...

Options:
  --input=FILE          file name of input font
  --output=FILE         file name of output font
  --version=VALUE       set font version to VALUE
  --feature-files=LIST  optional space delimited feature file list
  --classes=LIST        output a FEA file listing the specified glyph classes
  --css                 output is a CSS file
  --sfd                 output is a SFD file
  --web                 output is web optimised

  -h, --help            print this message and exit
""" % os.path.basename(sys.argv[0])

    print message
    sys.exit(code)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                "h",
                ["help","input=","output=", "feature-files=", "version=","classes=", "css", "web", "sfd"])
    except getopt.GetoptError, err:
        print str(err)
        usage(-1)

    infile = None
    outfile = None
    feafiles = None
    classes = None
    version = None
    css = False
    web = False
    sfd = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        elif opt == "--input": infile = arg
        elif opt == "--output": outfile = arg
        elif opt == "--feature-files": feafiles = arg
        elif opt == "--classes": classes = arg
        elif opt == "--version": version = arg
        elif opt == "--css": css = True
        elif opt == "--web": web = True
        elif opt == "--sfd": sfd = True

    if not infile:
        print "No input file"
        usage(-1)
    if not outfile:
        print "No output file"
        usage(-1)

    font = fontforge.open(infile)
    flags  = ("opentype", "dummy-dsig", "round")

    if css:
        #XXX hack
        base = os.path.splitext(os.path.basename(infile))[0]

        text = genCSS(font, base)
        font.close()

        out = open(outfile, "w")
        out.write(text)
        out.close()

        sys.exit(0)

    if classes:
        text = genClasses(font, classes)
        font.close()

        out = open(outfile, "w")
        out.write(text)
        out.close()

        sys.exit(0)

    if version:
        font.version = "%07.3f" %float(version)

    if sfd:
        font.save(outfile)
        font.close()

        sys.exit(0)

    if feafiles:
        oldfea = tempfile.mkstemp(suffix='.fea')[1]
        font.generateFeatureFile(oldfea)

        for lookup in font.gpos_lookups:
            font.removeLookup(lookup)

        for fea in feafiles.split():
            font.mergeFeature(fea)

        font.mergeFeature(oldfea)
        os.remove(oldfea)

    if web:
        # If we are building a web version then try to minimise file size

        # 'name' table is a bit bulky, and of almost no use in for web fonts,
        # so we strip all unnecessary entries.
        font.appendSFNTName ("English (US)", "License", "OFL v1.1")

        for name in font.sfnt_names:
            if name[0] == "Arabic (Egypt)":
                font.appendSFNTName(name[0], name[1], None)
            elif name[1] in ("Descriptor", "Sample Text"):
                font.appendSFNTName(name[0], name[1], None)

        for glyph in font.glyphs():
            # don't unlink transformed references
            glyph.unlinkRmOvrlpSave = 0
            # glyphs colored yellow are merely placeholders, so clear them to
            # save few kilobytes
            if glyph.color == 0xffff00:
                glyph.clear()
                glyph.width = 0

        # no dummy DSIG table nor glyph names
        flags  = ("opentype", "round", "short-post")

    font.generate(outfile, flags=flags)

if __name__ == "__main__":
    main()
