#!/usr/bin/python
# coding=utf-8
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
import subprocess

def genCSS(font, base):
    if font.fullname.lower().find("slanted")>0:
        style = "oblique"
    else:
        style = "normal"

    weight = font.os2_weight
    family = "%sWeb" %font.familyname
    name = font.fontname

    css = """
@font-face {
    font-family: %(family)s;
    font-style: %(style)s;
    font-weight: %(weight)s;
    src: url('%(base)s.eot?') format('eot'),
         url('%(base)s.woff') format('woff'),
         url('%(base)s.ttf')  format('truetype');
}
""" %{"style":style, "weight":weight, "family":family, "base":base}

    return css

def cleanAnchors(font):
    klasses = (
            "Dash",
            "DigitAbove",
            "DigitBelow",
            "DotAbove",
            "DotAlt",
            "DotBelow",
            "DotBelowAlt",
            "DotHmaza",
            "HighHamza",
            "MarkDotAbove",
            "MarkDotBelow",
            "RingBelow",
            "RingDash",
            "Stroke",
            "TaaAbove",
            "TaaBelow",
            "Tail",
            "TashkilAboveDot",
            "TashkilBelowDot",
            "TwoDotsAbove",
            "TwoDotsBelow",
            "TwoDotsBelowAlt"
            )

    for klass in klasses:
        subtable = font.getSubtableOfAnchor(klass)
        lookup = font.getLookupOfSubtable(subtable)
        font.removeLookup(lookup)

def validateGlyphs(font):
    flipped_ref = 0x10
    wrong_dir = 0x8
    missing_extrema = 0x20
    for glyph in font.glyphs():
        state = glyph.validate(True)
        if state & flipped_ref:
            glyph.unlinkRef()
            glyph.correctDirection()
        if state & wrong_dir:
            glyph.correctDirection()
        if state & missing_extrema:
            glyph.addExtrema("all")

def usage(code):
    message = """Usage: %s OPTIONS...

Options:
  --input=FILE          file name of input font
  --output=FILE         file name of output font
  --version=VALUE       set font version to VALUE
  --feature-file=FILE   optional feature file
  --slant=VALUE         autoslant
  --css                 output is a CSS file
  --sfd                 output is a SFD file
  --web                 output is web optimised
  --no-localised-name   strip out localised font name

  -h, --help            print this message and exit
""" % os.path.basename(sys.argv[0])

    print message
    sys.exit(code)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                "h",
                ["help","input=","output=", "feature-file=", "version=", "slant=", "css", "web", "sfd", "no-localised-name"])
    except getopt.GetoptError, err:
        print str(err)
        usage(-1)

    infile = None
    outfile = None
    feafile = None
    version = None
    slant = False
    css = False
    web = False
    sfd = False
    nolocalename = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        elif opt == "--input": infile = arg
        elif opt == "--output": outfile = arg
        elif opt == "--feature-file": feafile = arg
        elif opt == "--version": version = arg
        elif opt == "--slant": slant = float(arg)
        elif opt == "--css": css = True
        elif opt == "--web": web = True
        elif opt == "--sfd": sfd = True
        elif opt == "--no-localised-name": nolocalename = True

    if not infile:
        print "No input file"
        usage(-1)
    if not outfile:
        print "No output file"
        usage(-1)

    font = None

    if not (web or css):
        font = fontforge.open(infile)

    flags  = ("opentype", "dummy-dsig", "round")

    if css:
        text = ""
        files = infile.split()
        for f in files:
            base = os.path.splitext(os.path.basename(f))[0]
            font = fontforge.open(f)
            text += genCSS(font, base)
            font.close()

        out = open(outfile, "w")
        out.write(text)
        out.close()

        sys.exit(0)

    if version:
        font.version = "%07.3f" %float(version)
        font.appendSFNTName("Arabic (Egypt)", "Version", "إصدارة %s" %font.version.replace(".", ","))

    if sfd:
        font.save(outfile)
        font.close()

        sys.exit(0)

    if font and not slant:
        # remove anchors that are not needed in the production font
        cleanAnchors(font)

        # fix some common font issues
        validateGlyphs(font)

    if feafile:
        oldfea = tempfile.mkstemp(suffix='.fea')[1]
        font.generateFeatureFile(oldfea)

        for lookup in font.gpos_lookups:
            font.removeLookup(lookup)

        font.mergeFeature(feafile)
        font.mergeFeature(oldfea)
        os.remove(oldfea)

    if nolocalename:
        for name in font.sfnt_names:
            if name[0] != "English (US)" and name[1] in ("Family", "Fullname"):
                font.appendSFNTName(name[0], name[1], None)

    if slant:
        import psMat
        import math

        # compute amout of skew, magic formula copied from fontforge sources
        skew = psMat.skew(-slant * math.pi/180.0)

        font.selection.all()
        font.unlinkReferences()
        font.transform(skew)
        font.replaceWithReference()

        # fix metadata
        font.italicangle = slant
        font.fontname = font.fontname.replace("Regular", "Slanted")
        font.fullname += " Slanted"
        font.appendSFNTName("Arabic (Egypt)", "SubFamily", "مائل")

    if web:
        # If we are building a web version then try to minimise file size
        from fontTools.ttLib import TTFont
        font = TTFont(infile, recalcBBoxes=0)

        # internal glyph names are useless on the web, so force a format 3 post
        # table
        post = font['post']
        post.formatType = 3.0
        post.glyphOrder = None
        del(post.extraNames)
        del(post.mapping)

        # 'name' table is a bit bulky, and of almost no use in for web fonts,
        # so we strip all unnecessary entries.
        name = font['name']
        names = []
        for record in name.names:
            platID = record.platformID
            langID = record.langID
            nameID = record.nameID

            # we keep only en_US entries in Windows and Mac platform id, every
            # thing else is dropped
            if (platID == 1 and langID == 0) or (platID == 3 and langID == 1033):
                if nameID == 13:
                    # the full OFL text is too much, replace it with a simple
                    # string
                    if platID == 3:
                        # MS strings are UTF-16 encoded
                        text = 'OFL v1.1'.encode('utf_16_be')
                    else:
                        text = 'OFL v1.1'
                    record.string = text
                    names.append(record)
                # keep every thing else except Descriptor, Sample Text
                elif nameID not in (10, 19):
                    names.append(record)

        name.names = names

        # dummy DSIG is useless here too
        del(font['DSIG'])

        # FFTM is FontForge specific, remove too
        del(font['FFTM'])

        # force compiling GPOS/GSUB tables by fontTools, saves few tens of KBs
        for tag in ('GPOS', 'GSUB'):
            font[tag].compile(font)

        font.save(outfile)
        font.close()
    else:
        # ff takes long to write the file, so generate to tmp file then rename
        # it to keep fontview happy
        tmpout = tempfile.mkstemp(dir=".", suffix=os.path.basename(outfile))[1]
        font.generate(tmpout, flags=flags)
        font.close()
        #os.rename(tmpout, outfile) # file monitor will not see this, why?
        p = subprocess.Popen("cat %s > %s" %(tmpout, outfile), shell=True)
        p.wait()
        os.remove(tmpout)

if __name__ == "__main__":
    main()
