#!/usr/bin/python

import fontforge
import sys
import os
import getopt

def genCSS(font, base):
    if font.fullname.lower().find("slanted")>0:
        style = "slanted"
    else:
        style = "normal"

    weight = font.os2_weight
    family = "%sWeb" %font.familyname
    name = font.fontname

    css = ""
    css += """
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

def doKern(font, remove):
    """Looks for any kerning classes in the font and converts it to
    RTL kerning pairs."""
    new_subtable = ""
    for lookup in font.gpos_lookups:
        if font.getLookupInfo(lookup)[0] == "gpos_pair":
            for subtable in font.getLookupSubtables(lookup):
                if font.isKerningClass(subtable):
                    new_subtable = subtable + " pairs"
                    font.addLookupSubtable(lookup, new_subtable)
                    kclass   = font.getKerningClass(subtable)
                    klasses1 = kclass[0]
                    klasses2 = kclass[1]
                    offsets  = kclass[2]

                    for klass1 in klasses1:
                        if klass1 != None:
                            for name in klass1:
                                glyph = font.createChar(-1, name)
                                for klass2 in klasses2:
                                    if klass2 != None:
                                        kern = offsets[klasses1.index(klass1)
                                                *len(klasses2)+
                                                klasses2.index(klass2)]
                                        if kern != 0:
                                            for glyph2 in klass2:
                                                glyph.addPosSub(new_subtable,
                                                        glyph2,
                                                        kern,0,kern,0,0,0,0,0)
					        font.changed = True
                    if remove:
                        font.removeLookupSubtable(subtable)
    return new_subtable

def usage(code):
    message = """Usage: %s OPTIONS...

Options:
  -i, --input=FILE          file name of input font
  -o, --output=FILE         file name of output font
  -f, --feature-files=LIST  optional space delimited feature file list
  -c, --css                 output is a CSS file
  -s, --sfd                 output is a SFD file
  -w, --web                 output is web optimised
  -v, --font-version=VALUE  set font version to VALUE

  -h, --help                print this message and exit
""" % os.path.basename(sys.argv[0])

    print message
    sys.exit(code)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                "hi:o:f:v:cws",
                ["help","input=","output=", "feature-files=", "font-version", "css", "web", "sfd"])
    except getopt.GetoptError, err:
        print str(err)
        usage(-1)

    infile = None
    outfile = None
    feafiles = None
    version = None
    css = False
    web = False
    sfd = False

    for o, a in opts:
        if o in ("-h", "--help"):
            usage(0)
        elif o in ("-i", "--input"):
            infile = a
        elif o in ("-o", "--output"):
            outfile = a
        elif o in ("-f", "--feature-files"):
            feafiles = a
        elif o in ("-v", "--font-version"):
            version = a
        elif o in ("-c", "--css"):
            css = True
        elif o in ("-w", "--web"):
            web = True
        elif o in ("-s", "--sfd"):
            sfd = True

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

    if version:
        font.version = "%07.3f" %float(version)

    if sfd:
        font.save(outfile)
        font.close()

        sys.exit(0)

    if feafiles:
        for fea in feafiles.split():
            font.mergeFeature(fea)

    if web:
        font.appendSFNTName ("English (US)", "License", "OFL v1.1")
        flags  = ("opentype", "round", "short-post")

    doKern(font, True)
    font.generate(outfile, flags=flags)

if __name__ == "__main__":
    main()
