#!/usr/bin/python
# coding=utf-8
#
# build.py - Amiri font build utility
#
# Written in 2010-2012 by Khaled Hosny <khaledhosny@eglug.org>
#
# To the extent possible under law, the author have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import fontforge
import psMat
import sys
import os
import getopt
import math
import unicodedata as ucd
from tempfile import mkstemp
from fontTools.ttLib import TTFont

def genCSS(font, base):
    """Generates a CSS snippet for webfont usage based on:
    http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax"""

    style = ("slanted" in font.fullname.lower()) and "oblique" or "normal"
    weight = font.os2_weight
    family = font.familyname + "Web"

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
    """Removes anchor classes (and associated lookups) that are used only
    internally for building composite glyph."""

    klasses = (
            "Dash",
            "DigitAbove",
            "DigitBelow",
            "DotAbove",
            "DotAlt",
            "DotBelow",
            "DotBelowAlt",
            "DotHmaza",
            "HamzaBelow",
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
            "TwoDotsBelowAlt",
            "VAbove",
            )

    for klass in klasses:
        subtable = font.getSubtableOfAnchor(klass)
        lookup = font.getLookupOfSubtable(subtable)
        font.removeLookup(lookup)

def flattenNestedReferences(font, ref, new_transform=None):
    """Flattens nested references by replacing them with the ultimate reference
    and applying any transformation matrices involved, so that the final font
    has only simple composite glyphs. This to work around what seems to be an
    Apple bug that results in ignoring transformation matrix of nested
    references."""

    name = ref[0]
    transform = ref[1]
    glyph = font[name]
    new_ref = []
    if glyph.references and glyph.foreground.isEmpty():
        for nested_ref in glyph.references:
            for i in flattenNestedReferences(font, nested_ref, transform):
                new_ref.append(i)
    else:
        if new_transform:
            matrix = psMat.compose(transform, new_transform)
            new_ref.append((name, matrix))
        else:
            new_ref.append(ref)

    return new_ref

def validateGlyphs(font):
    """Fixes some common FontForge validation warnings, currently handles:
        * wrong direction
        * flipped references
        * missing points at extrema
    In addition to flattening nested references."""

    wrong_dir = 0x8
    flipped_ref = 0x10
    missing_extrema = 0x20
    for glyph in font.glyphs():
        state = glyph.validate(True)
        refs = []

        if state & flipped_ref:
            glyph.unlinkRef()
            glyph.correctDirection()
        if state & wrong_dir:
            glyph.correctDirection()
        if state & missing_extrema:
            glyph.addExtrema("all")

        for ref in glyph.references:
            for i in flattenNestedReferences(font, ref):
                refs.append(i)
        if refs:
            glyph.references = refs

def setVersion(font, version):
    font.version = "%07.3f" % float(version)
    for name in font.sfnt_names:
        if name[0] == "Arabic (Egypt)" and name[1] == "Version":
            font.appendSFNTName(name[0], name[1],
                                name[2].replace("VERSION", font.version.replace(".", "\xD9\xAB")))

def mergeFeatures(font, feafile):
    """Merges feature file into the font while making sure mark positioning
    lookups (already in the font) come after kerning lookups (from the feature
    file), which is required by Uniscribe to get correct mark positioning for
    kerned glyphs."""

    oldfea = mkstemp(suffix='.fea')[1]
    font.generateFeatureFile(oldfea)

    for lookup in font.gpos_lookups:
        font.removeLookup(lookup)

    font.mergeFeature(feafile)
    font.mergeFeature(oldfea)
    os.remove(oldfea)

def makeCss(infiles, outfile):
    """Builds a CSS file for the entire font family."""

    css = ""

    for f in infiles.split():
        base = os.path.splitext(os.path.basename(f))[0]
        font = fontforge.open(f)
        css += genCSS(font, base)
        font.close()

    out = open(outfile, "w")
    out.write(css)
    out.close()

def generateFont(font, outfile, hack=False):
    flags  = ("opentype", "dummy-dsig", "round")

    if hack:
        # ff takes long to write the file, so generate to tmp file then rename
        # it to keep fontview happy
        import subprocess
        tmpout = mkstemp(dir=".", suffix=os.path.basename(outfile))[1]
        font.generate(tmpout, flags=flags)
        #os.rename(tmpout, outfile) # file monitor will not see this, why?
        p = subprocess.Popen("cat %s > %s" %(tmpout, outfile), shell=True)
        p.wait()
        os.remove(tmpout)
    else:
        font.generate(outfile, flags=flags)
    font.close()

def drawOverUnderline(glyph, pos, thickness, width):
    pen = glyph.glyphPen()

    pen.moveTo((-50, pos))
    pen.lineTo((-50, pos + thickness))
    pen.lineTo((width + 50, pos + thickness))
    pen.lineTo((width + 50, pos))
    pen.closePath()

def makeOverUnderline(font):
    # test string:
    # صِ̅فْ̅ ̅خَ̅ل̅قَ̅ ̅بًّ̅ صِ̲فْ̲ ̲خَ̲ل̲قَ̲ ̲بِ̲

    thickness = font.uwidth # underline width (thickness)
    o_pos = font.os2_typoascent
    u_pos = font.upos - thickness # underline pos
    minwidth = 100.0

    widths = {}

    for glyph in font.glyphs():
        if glyph.glyphclass == 'baseglyph':
            width = round(glyph.width/100) * 100
            width = width > minwidth and width or minwidth
            if not width in widths:
                widths[width] = []
            widths[width].append(glyph.glyphname)

    o_encoded = font.createChar(0x0305, 'uni0305')
    u_encoded = font.createChar(0x0332, 'uni0332')
    o_encoded.width = u_encoded.width = 0
    o_encoded.glyphclass = u_encoded.glyphclass = 'mark'
    drawOverUnderline(o_encoded, o_pos, thickness, 500)
    drawOverUnderline(u_encoded, u_pos, thickness, 500)

    o_base = font.createChar(-1, 'uni0305.0')
    u_base = font.createChar(-1, 'uni0332.0')
    o_base.width = u_base.width = 0
    o_base.glyphclass = u_base.glyphclass = 'baseglyph'
    drawOverUnderline(o_base, o_pos, thickness, 500)
    drawOverUnderline(u_base, u_pos, thickness, 500)

    font.addLookup('mark hack', 'gsub_single', (), (("mark",(("arab",("dflt")),)),), font.gsub_lookups[-1])
    font.addLookupSubtable('mark hack', 'mark hack 1')

    o_encoded.addPosSub('mark hack 1', o_base.glyphname)
    u_encoded.addPosSub('mark hack 1', u_base.glyphname)

    context_lookup_name = 'OverUnderLine'
    font.addLookup(context_lookup_name, 'gsub_contextchain', ('ignore_marks'), (("mark",(("arab",("dflt")),)),), font.gsub_lookups[-1])

    for width in sorted(widths.keys()):
        o_name = 'uni0305.%d' % width
        u_name = 'uni0332.%d' % width
        o_glyph = font.createChar(-1, o_name)
        u_glyph = font.createChar(-1, u_name)

        o_glyph.glyphclass = u_glyph.glyphclass = 'mark'

        drawOverUnderline(o_glyph, o_pos, thickness, width)
        drawOverUnderline(u_glyph, u_pos, thickness, width)

        single_lookup_name = str(width)

        font.addLookup(single_lookup_name, 'gsub_single', (), (), font.gsub_lookups[-1])
        font.addLookupSubtable(single_lookup_name, single_lookup_name + '1')

        o_base.addPosSub(single_lookup_name + '1', o_name)
        u_base.addPosSub(single_lookup_name + '1', u_name)

        rule = '| [%s] [%s %s] @<%s> | ' %(" ".join(widths[width]), o_base.glyphname, u_base.glyphname, single_lookup_name)

        font.addContextualSubtable(context_lookup_name, context_lookup_name + str(width), 'coverage', rule)

def mergeLatin(font):
    styles = {"Regular": "Roman",
              "Slanted": "Italic",
              "Bold": "Bold",
              "BoldSlanted": "BoldItalic"}

    latinfile = "Crimson-%s.sfd" %styles[font.fontname.split("-")[1]]

    tmpfont = mkstemp(suffix=os.path.basename(latinfile))[1]
    latinfont = fontforge.open("sources/crimson/%s" %latinfile)
    latinfont.em = 2048

    validateGlyphs(latinfont) # to flatten nested refs mainly

    # collect latin glyphs we want to keep
    latinglyphs = []

    # we want all glyphs in latin0-9 encodings
    for i in range(0, 9):
        latinfont.encoding = 'latin%d' %i
        for glyph in latinfont.glyphs("encoding"):
            if glyph.encoding <= 255:
                if glyph.glyphname not in latinglyphs:
                    latinglyphs.append(glyph.glyphname)
            elif glyph.unicode != -1 and glyph.unicode <= 0x017F:
                # keep also Unicode Latin Extended-A block
                if glyph.glyphname not in latinglyphs:
                    latinglyphs.append(glyph.glyphname)

    # keep ligatures too
    ligatures = ("f_f", "f_i", "f_f_i", "f_l", "f_f_l", "f_b", "f_f_b", "f_k",
            "f_f_k", "f_h", "f_f_h", "f_j", "f_f_j", "T_h")

    # and Arabic romanisation characters
    romanisation = ("afii57929", "uni02BE", "uni02BE", "amacron", "uni02BE",
            "amacron", "eacute", "uni1E6F", "ccedilla", "uni1E6F", "gcaron",
            "ycircumflex", "uni1E29", "uni1E25", "uni1E2B", "uni1E96",
            "uni1E0F", "dcroat", "scaron", "scedilla", "uni1E63", "uni1E11",
            "uni1E0D", "uni1E6D", "uni1E93", "dcroat", "uni02BB", "uni02BF",
            "rcaron", "grave", "gdotaccent", "gbreve", "umacron", "imacron",
            "amacron", "amacron", "uni02BE", "amacron", "uni02BE",
            "acircumflex", "amacron", "uni1E97", "tbar", "aacute", "amacron",
            "ygrave", "agrave", "uni02BE", "aacute")

    # and some typographic characters
    typographic = ("uni2010", "uni2011", "figuredash", "endash", "emdash",
            "afii00208", "quoteleft", "quoteright", "quotesinglbase",
            "quotereversed", "quotedblleft", "quotedblright", "quotedblbase",
            "uni201F", "dagger", "daggerdbl", "bullet", "onedotenleader",
            "ellipsis", "uni202F", "perthousand", "minute", "second",
            "uni2038", "guilsinglleft", "guilsinglright", "uni203E",
            "fraction")

    for l in (ligatures, romanisation, typographic):
        for name in l:
            if name not in latinglyphs:
                latinglyphs.append(name)

    # keep any glyph referenced by previous glyphs
    for name in latinglyphs:
        if name in latinfont:
            glyph = latinfont[name]
            for ref in glyph.references:
                latinglyphs.append(ref[0])
        else:
            print 'Font ‘%s’ is missing glyph: %s' %(font.fontname, name)

    # remove everything else
    for glyph in latinfont.glyphs():
        if glyph.glyphname not in latinglyphs:
            latinfont.removeGlyph(glyph)

    kern_lookups = {}
    # remove names of removed glyphs from kern classes
    for lookup in latinfont.gpos_lookups:
        kern_lookups[lookup] = {}
        kern_lookups[lookup]["subtables"] = []
        kern_lookups[lookup]["type"], kern_lookups[lookup]["flags"], kern_lookups[lookup]["langsys"] = latinfont.getLookupInfo(lookup)
        for subtable in latinfont.getLookupSubtables(lookup):
            if latinfont.isKerningClass(subtable):
                old_first, old_second, old_offsets = latinfont.getKerningClass(subtable)
                new_first = []
                new_second = []
                new_offsets = []

                cnt1 = len(old_first)
                cnt2 = len(old_second)

                # group offsets into tuples per class
                offsets = []
                i = 0
                while i < cnt1 * cnt2:
                    offsets.append(list(old_offsets[i:i+cnt2]))
                    i += cnt2

                # drop missing glyphs
                for klass in old_first:
                    new_klass = []
                    if klass:
                        for name in klass:
                            if name in latinfont:
                                new_klass.append(name)
                    if new_klass:
                        new_first.append(new_klass)
                    else:
                        new_first.append(None)

                for klass in old_second:
                    new_klass = []
                    if klass:
                        for name in klass:
                            if name in latinfont:
                                new_klass.append(name)
                    if new_klass:
                        new_second.append(new_klass)
                    else:
                        new_second.append(None)

                # drop empty classes
                while None in new_first:
                    i = new_first.index(None)
                    new_first.pop(i)
                    offsets.pop(i)

                while None in new_second:
                    i = new_second.index(None)
                    new_second.pop(i)
                    for j in offsets:
                        j.pop(i)

                for i in offsets:
                    new_offsets.extend(i)

                if new_first and new_second and new_offsets:
                    kern_lookups[lookup]["subtables"].append((subtable, (new_first, new_second, new_offsets)))

    for glyph in latinfont.glyphs():
        if glyph.glyphname != "space" and glyph.glyphname in font:
            latinfont.selection.select(glyph.glyphname)
            latinfont.copy()
            font.selection.select(glyph.glyphname)
            font.paste()

    for lookup in latinfont.gpos_lookups:
        latinfont.removeLookup(lookup)

    tmpfea = mkstemp(suffix='.fea')[1]
    latinfont.generateFeatureFile(tmpfea)

    for lookup in latinfont.gsub_lookups:
        latinfont.removeLookup(lookup)

    latinfont.save(tmpfont)
    latinfont.close()

    font.mergeFonts(tmpfont)
    font.mergeFeature(tmpfea)

    os.remove(tmpfont)
    os.remove(tmpfea)

    for ltr, rtl in (("question", "uni061F"), ("radical", "radical.rtlm")):
        font[rtl].clear()
        font[rtl].addReference(ltr, psMat.scale(-1, 1))
        font[rtl].left_side_bearing = font[ltr].right_side_bearing
        font[rtl].right_side_bearing = font[ltr].left_side_bearing

    for lookup in kern_lookups:
        font.addLookup(lookup,
                kern_lookups[lookup]["type"],
                kern_lookups[lookup]["flags"],
                kern_lookups[lookup]["langsys"])

        for subtable in kern_lookups[lookup]["subtables"]:
            font.addKerningClass(lookup, subtable[0], subtable[1][0], subtable[1][1], subtable[1][2])

def makeWeb(infile, outfile):
    """If we are building a web version then try to minimise file size"""

    # "short-post" generates a post table without glyph names to save some KBs
    # since glyph names are only needed for PDF's as readers use them to
    # "guess" characters when copying text, which is of little use in web fonts.
    flags = ("opentype", "short-post")

    font = fontforge.open(infile)

    # removed compatibility glyphs that of little use on the web
    compat_ranges = (
            (0xfb50, 0xfbb1),
            (0xfbd3, 0xfd3d),
            (0xfd50, 0xfdf9),
            (0xfdfc, 0xfdfc),
            (0xfe70, 0xfefc),
            )

    for glyph in font.glyphs():
        for i in compat_ranges:
            start = i[0]
            end = i[1]
            if start <= glyph.unicode <= end:
                font.removeGlyph(glyph)
                break

    tmpfont = mkstemp(suffix=os.path.basename(outfile))[1]
    font.generate(tmpfont, flags=flags)
    font.close()

    # now open in fontTools
    font = TTFont(tmpfont, recalcBBoxes=0)

    # our 'name' table is a bit bulky, and of almost no use in for web fonts,
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

    # FFTM is FontForge specific, remove it
    del(font['FFTM'])

    # force compiling GPOS/GSUB tables by fontTools, saves few tens of KBs
    for tag in ('GPOS', 'GSUB'):
        font[tag].compile(font)

    font.save(outfile)
    font.close()

    os.remove(tmpfont)

def makeSlanted(infile, outfile, version, slant):

    font = makeDesktop(infile, outfile, version, False, False)

    # compute amout of skew, magic formula copied from fontforge sources
    skew = psMat.skew(-slant * math.pi/180.0)

    font.selection.all()

    for glyph in font.glyphs():
        u = glyph.unicode
        if u == -1:
            if '.' in glyph.glyphname:
                n = glyph.glyphname.split('.')[0]
                u = fontforge.unicodeFromName(n)
            if '_' in glyph.glyphname:
                for n in glyph.glyphname.split('_'):
                    uu = fontforge.unicodeFromName(n)
                    if uu != -1:
                        u = uu

        if u != -1:
            c = ucd.bidirectional(unichr(u))
            if c in ("L", "EN", "AN", "ES", "ET", "CS", "NSM", "BN", "ON"):
                font.selection.select(("less", None), glyph)

    font.transform(skew)

    # fix metadata
    font.italicangle = slant
    font.fullname += " Slanted"
    if font.weight == "Bold":
        font.fontname = font.fontname.replace("Bold", "BoldSlanted")
        font.appendSFNTName("Arabic (Egypt)", "SubFamily", "عريض مائل")
        font.appendSFNTName("English (US)",   "SubFamily", "Bold Slanted")
    else:
        font.fontname = font.fontname.replace("Regular", "Slanted")
        font.appendSFNTName("Arabic (Egypt)", "SubFamily", "مائل")

    mergeLatin(font)

    generateFont(font, outfile)

def makeDesktop(infile, outfile, version, latin=True, generate=True):
    font = fontforge.open(infile)

    if version:
        setVersion(font, version)

    # remove anchors that are not needed in the production font
    cleanAnchors(font)

    # fix some common font issues
    validateGlyphs(font)

    if font.sfd_path:
        feafile = os.path.splitext(font.sfd_path)[0] + '.fea'
        mergeFeatures(font, feafile)

    #makeOverUnderline(font)

    # sample text to be used by font viewers
    sample = 'صِفْ خَلْقَ خَوْدٍ كَمِثْلِ ٱلشَّمْسِ إِذْ بَزَغَتْ يَحْظَىٰ ٱلضَّجِيعُ بِهَا نَجْلَاءَ مِعْطَارِ.'

    for lang in ('Arabic (Egypt)', 'English (US)'):
        font.appendSFNTName(lang, 'Sample Text', sample)

    if latin:
        mergeLatin(font)

    if generate:
        generateFont(font, outfile, True)
    else:
        return font

def usage(extramessage, code):
    if extramessage:
        print extramessage

    message = """Usage: %s OPTIONS...

Options:
  --input=FILE          file name of input font
  --output=FILE         file name of output font
  --version=VALUE       set font version to VALUE
  --slant=VALUE         autoslant
  --css                 output is a CSS file
  --web                 output is web version

  -h, --help            print this message and exit
""" % os.path.basename(sys.argv[0])

    print message
    sys.exit(code)

if __name__ == "__main__":
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                "h",
                ["help","input=","output=", "version=", "slant=", "css", "web"])
    except getopt.GetoptError, err:
        usage(str(err), -1)

    infile = None
    outfile = None
    version = None
    slant = False
    css = False
    web = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage("", 0)
        elif opt == "--input": infile = arg
        elif opt == "--output": outfile = arg
        elif opt == "--version": version = arg
        elif opt == "--slant": slant = float(arg)
        elif opt == "--css": css = True
        elif opt == "--web": web = True

    if not infile:
        usage("No input file", -1)
    if not outfile:
        usage("No output file", -1)

    if css:
        makeCss(infile, outfile)
    elif web:
        makeWeb(infile, outfile)
    else:
        if not version:
            usage("No version specified", -1)

        if slant:
            makeSlanted(infile, outfile, version, slant)
        else:
            makeDesktop(infile, outfile, version)
