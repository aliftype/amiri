#!/usr/bin/env python
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

from __future__ import print_function

import fontforge
import psMat
import os

from tempfile import NamedTemporaryFile

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

def flattenNestedReferences(font, ref, new_transform=(1, 0, 0, 1, 0, 0)):
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
                matrix = psMat.compose(i[1], new_transform)
                new_ref.append((i[0], matrix))
    else:
        matrix = psMat.compose(transform, new_transform)
        new_ref.append((name, matrix))

    return new_ref

def validateGlyphs(font):
    """Fixes some common FontForge validation warnings, currently handles:
        * wrong direction
        * flipped references
    In addition to flattening nested references."""

    wrong_dir = 0x8
    flipped_ref = 0x10
    for glyph in font.glyphs():
        state = glyph.validate(True)
        refs = []

        if state & flipped_ref:
            glyph.unlinkRef()
            glyph.correctDirection()
        if state & wrong_dir:
            glyph.correctDirection()

        for ref in glyph.references:
            for i in flattenNestedReferences(font, ref):
                refs.append(i)
        if refs:
            glyph.references = refs

        glyph.round()

def updateInfo(font, version):
    from datetime import datetime

    version = "%07.3f" % version
    font.version = font.version % version
    font.copyright = font.copyright % datetime.now().year
    font.appendSFNTName("English (US)", "UniqueID", "%s;%s;%s" % (
        version, font.os2_vendor, font.fontname))

def generateFeatureString(font, lookup):
    with NamedTemporaryFile() as tmp:
        font.generateFeatureFile(tmp.name, lookup)
        fea = tmp.read()
        return fea.decode("utf-8")

def generateFeatures(font, feafile):
    """Generates feature text by merging feature file with mark positioning
    lookups (already in the font) and making sure they come after kerning
    lookups (from the feature file), which is required by Uniscribe to get
    correct mark positioning for kerned glyphs."""

    oldfea = ""
    for lookup in font.gpos_lookups:
        oldfea += generateFeatureString(font, lookup)

    for lookup in font.gpos_lookups + font.gsub_lookups:
        font.removeLookup(lookup)

    # open feature file and insert the generated GPOS features in place of the
    # placeholder text
    with open(feafile, 'rb') as fea:
        fea_text = fea.read().decode("utf-8")
    fea_text = fea_text.replace("{%anchors%}", oldfea)

    bases = [g.glyphname for g in font.glyphs() if g.glyphclass != "mark"]
    marks = [g.glyphname for g in font.glyphs() if g.glyphclass == "mark"]
    carets = {g.glyphname: g.lcarets for g in font.glyphs() if any(g.lcarets)}
    gdef = []
    gdef.append("@GDEFBase = [%s];" % " ".join(bases))
    gdef.append("@GDEFMark = [%s];" % " ".join(marks))
    gdef.append("table GDEF {")
    gdef.append("  GlyphClassDef @GDEFBase, , @GDEFMark, ;")
    for k, v in carets.items():
        gdef.append("  LigatureCaretByPos %s %s;" % (k, " ".join(map(str, v))))
    gdef.append("} GDEF;")

    fea_text += "\n".join(gdef)

    return fea_text

def generateFont(options, font, feastring):
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    from fontTools.ttLib import TTFont

    fea = generateFeatures(font, args.features)
    fea += feastring

    flags = ["opentype", "dummy-dsig", "round", "omit-instructions"]

    font.selection.all()
    font.correctReferences()
    font.selection.none()

    # fix some common font issues
    validateGlyphs(font)

    updateInfo(font, args.version)

    font.generate(args.output, flags=flags)

    try:
        ttfont = TTFont(args.output)
        addOpenTypeFeaturesFromString(ttfont, fea)

        # Filter-out useless Macintosh names
        name = ttfont["name"]
        name.names = [n for n in name.names if n.platformID != 1]

        # Drop useless table with timestamp
        if "FFTM" in ttfont:
            del ttfont["FFTM"]
        ttfont.save(args.output)
    except:
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(fea.encode("utf-8"))
            print("Failed! Inspect temporary file: %r" % tmp.name)
            os.remove(args.output)
        raise


def drawOverline(font, name, uni, pos, thickness, width):
    glyph = font.createChar(uni, name)
    glyph.width = 0
    glyph.glyphclass = "mark"

    pen = glyph.glyphPen()

    pen.moveTo((-50, pos))
    pen.lineTo((-50, pos + thickness))
    pen.lineTo((width + 50, pos + thickness))
    pen.lineTo((width + 50, pos))
    pen.closePath()

    return glyph

def makeQuranSajdaLine(font, pos):
    # test string:
    # صِ̅فْ̅ ̅خَ̅ل̅قَ̅ ̅بًّ̅ صِ̲فْ̲ ̲خَ̲ل̲قَ̲ ̲بِ̲

    thickness = font.uwidth # underline width (thickness)
    minwidth = 100

    # collect glyphs grouped by their widths rounded by 100 units, we will use
    # them to decide the widths of over/underline glyphs we will draw
    widths = {}
    for glyph in font.glyphs():
        u = glyph.unicode
        if ((u < 0) or (0x0600 <= u <= 0x06FF) or u == ord(" ")) \
        and glyph.width > 0:
            width = round(glyph.width / minwidth) * minwidth
            width = width > minwidth and width or minwidth
            if not width in widths:
                widths[width] = []
            widths[width].append(glyph.glyphname)

    base = 'uni0305'
    drawOverline(font, base, 0x0305, pos, thickness, 500)

    fea = []
    fea.append("@OverSet = [%s];" % base)
    fea.append("feature mark {")
    fea.append("  lookupflag UseMarkFilteringSet @OverSet;")

    for width in sorted(widths.keys()):
        # for each width group we create an over/underline glyph with the same
        # width, and add a contextual substitution lookup to use it when an
        # over/underline follows any glyph in this group
        name = 'uni0305.%d' % width
        drawOverline(font, name, -1, pos, thickness, width)
        fea.append("  sub [%s] %s' by %s;" % (" ".join(widths[width]), base, name))

    fea.append("} mark;")

    fea = "\n".join(fea)
    return fea

def centerGlyph(glyph):
    width = glyph.width
    glyph.right_side_bearing = glyph.left_side_bearing = (glyph.right_side_bearing + glyph.left_side_bearing)/2
    glyph.width = width

def subsetFont(font, glyphnames, similar=False):
    # keep any glyph with the same base name
    reported = []

    if similar:
        for name in glyphnames:
            for glyph in font.glyphs():
                if "." in glyph.glyphname and glyph.glyphname.split(".")[0] == name:
                    glyphnames.append(glyph.glyphname)

    # keep any glyph referenced requested glyphs
    for name in glyphnames:
        if name in font:
            glyph = font[name]
            for ref in glyph.references:
                glyphnames.append(ref[0])
        else:
            if name not in reported:
                print('Font ‘%s’ is missing glyph: %s' %(font.fontname, name))
                reported.append(name)

    # Prune kerning classes
    for lookup in font.gpos_lookups:
        for subtable in font.getLookupSubtables(lookup):
            if font.isKerningClass(subtable):
                first, second, offsets = font.getKerningClass(subtable)
                first  = [[n for n in c if n in glyphnames] for c in first]
                second = [[n for n in c if n in glyphnames] for c in second if c]
                second.insert(0, None)
                if all([first, second]):
                    font.alterKerningClass(subtable, first, second, offsets)
                else:
                    font.removeLookupSubtable(subtable)

    # remove everything else
    for glyph in font.glyphs():
        if glyph.glyphname not in glyphnames:
            font.removeGlyph(glyph)

def subsetFontFT(path, unicodes, quran=False):
    from fontTools.ttLib import TTFont
    from fontTools import subset

    font = TTFont(path)

    options = subset.Options()
    options.set(layout_features='*', name_IDs='*', name_languages='*',
        notdef_outline=True, glyph_names=True)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    if quran:
        font["OS/2"].sTypoAscender = font["hhea"].ascent = font["head"].yMax

    font.save(path)

def makeNumerators(font):
    digits = ("zero", "one", "two", "three", "four", "five", "six", "seven",
              "eight", "nine",
              "uni0660", "uni0661", "uni0662", "uni0663", "uni0664",
              "uni0665", "uni0666", "uni0667", "uni0668", "uni0669",
              "uni06F0", "uni06F1", "uni06F2", "uni06F3", "uni06F4",
              "uni06F5", "uni06F6", "uni06F7", "uni06F8", "uni06F9",
              "uni06F4.urd", "uni06F6.urd", "uni06F7.urd")
    for name in digits:
        numr = font.createChar(-1, name + ".numr")
        small = font[name + ".small"]
        if not numr.isWorthOutputting():
            numr.clear()
            numr.addReference(small.glyphname, psMat.translate(0, 550))
            numr.width = small.width

def mergeLatin(font, italic=False, glyphs=None, quran=False):
    styles = {"Regular": "Regular",
              "Slanted": "Italic",
              "Bold": "Bold",
              "BoldSlanted": "BoldItalic"}

    style = styles[font.fontname.split("-")[1]]

    latinfile = "AmiriLatin-%s.sfdir" %style

    from tempfile import mkstemp
    tmpfont = mkstemp(suffix=os.path.basename(latinfile).replace("sfdir", "sfd"))[1]
    latinfont = fontforge.open("sources/latin/%s" %latinfile)

    validateGlyphs(latinfont) # to flatten nested refs mainly

    if glyphs:
        latinglyphs = list(glyphs)
    else:
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
                elif glyph.unicode == -1 and '.prop' in glyph.glyphname:
                    # proportional digits
                    latinglyphs.append(glyph.glyphname)

        # keep ligatures too
        ligatures = ("f_b", "f_f_b",
                     "f_h", "f_f_h",
                     "f_i", "f_f_i",
                     "f_j", "f_f_j",
                     "f_k", "f_f_k",
                     "f_l", "f_f_l",
                     "f_f")

        # and Arabic romanisation characters
        romanisation = ("uni02BC", "uni02BE", "uni02BE", "amacron", "uni02BE",
                "amacron", "eacute", "uni1E6F", "ccedilla", "uni1E6F", "gcaron",
                "ycircumflex", "uni1E29", "uni1E25", "uni1E2B", "uni1E96",
                "uni1E0F", "dcroat", "scaron", "scedilla", "uni1E63", "uni1E11",
                "uni1E0D", "uni1E6D", "uni1E93", "dcroat", "uni02BB", "uni02BF",
                "rcaron", "grave", "gdotaccent", "gbreve", "umacron", "imacron",
                "amacron", "amacron", "uni02BE", "amacron", "uni02BE",
                "acircumflex", "amacron", "uni1E97", "tbar", "aacute", "amacron",
                "ygrave", "agrave", "uni02BE", "aacute", "Amacron", "Amacron",
                "Eacute", "uni1E6E", "Ccedilla", "uni1E6E", "Gcaron",
                "Ycircumflex", "uni1E28", "uni1E24", "uni1E2A", "uni1E0E",
                "Dcroat", "Scaron", "Scedilla", "uni1E62", "uni1E10", "uni1E0C",
                "uni1E6C", "uni1E92", "Dcroat", "Rcaron", "Gdotaccent", "Gbreve",
                "Umacron", "Imacron", "Amacron", "Amacron", "Amacron",
                "Acircumflex", "Amacron", "Tbar", "Aacute", "Amacron", "Ygrave",
                "Agrave", "Aacute")

        # and some typographic characters
        typographic = ("uni2010", "uni2011", "figuredash", "endash", "emdash",
                "uni2015", "quoteleft", "quoteright", "quotesinglbase",
                "quotereversed", "quotedblleft", "quotedblright", "quotedblbase",
                "uni201F", "dagger", "daggerdbl", "bullet", "onedotenleader",
                "ellipsis", "uni202F", "perthousand", "minute", "second",
                "uni2038", "guilsinglleft", "guilsinglright", "uni203E",
                "fraction", "i.TRK", "minus", "uni2213", "radical", "uni2042")

        for l in (ligatures, romanisation, typographic):
            for name in l:
                if name not in latinglyphs:
                    latinglyphs.append(name)

    if not quran:
        # we want our ring above and below in Quran font only
        for name in ("uni030A", "uni0325"):
            font.removeGlyph(name)

    subsetFont(latinfont, latinglyphs)

    digits = ("zero", "one", "two", "three", "four", "five", "six", "seven",
              "eight", "nine")

    # common characters that can be used in Arabic and Latin need to be handled
    # carefully in the slanted font so that right leaning italic is used with
    # Latin, and left leaning slanted is used with Arabic, using ltra and rtla
    # features respectively, for less OpenType savvy apps we make the default
    # upright so it works reasonably with bot scripts
    if italic:
        if "bold" in style:
            upright = fontforge.open("sources/latin/AmiriLatin-Bold.sfdir")
        else:
            upright = fontforge.open("sources/latin/AmiriLatin-Regular.sfdir")

        shared = ("exclam", "quotedbl", "numbersign", "dollar", "percent",
                  "quotesingle", "asterisk", "plus", "colon", "semicolon",
                  "less", "equal", "greater", "question", "at", "asciicircum",
                  "exclamdown", "section", "copyright", "logicalnot", "registered",
                  "plusminus", "uni00B2", "uni00B3", "paragraph", "uni00B9",
                  "ordmasculine", "onequarter", "onehalf", "threequarters",
                  "questiondown", "quoteleft", "quoteright", "quotesinglbase",
                  "quotereversed", "quotedblleft", "quotedblright",
                  "quotedblbase", "uni201F", "dagger", "daggerdbl",
                  "perthousand", "minute", "second", "guilsinglleft",
                  "guilsinglright", "fraction", "uni2213")

        for name in shared:
            glyph = latinfont[name]
            glyph.clear()
            upright.selection.select(name)
            upright.copy()
            latinfont.createChar(upright[name].encoding, name)
            latinfont.selection.select(name)
            latinfont.paste()

        for name in digits:
            glyph = latinfont[name]
            glyph.glyphname += '.ltr'
            glyph.unicode = -1
            upright.selection.select(name)
            upright.copy()
            latinfont.createChar(upright[name].encoding, name)
            latinfont.selection.select(name)
            latinfont.paste()

            rtl = latinfont.createChar(-1, name + ".rtl")
            rtl.addReference(name, italic)
            rtl.useRefsMetrics(name)

        for name in digits:
            pname = name + ".prop"
            glyph = latinfont[pname]
            glyph.glyphname = name + '.ltr.prop'
            glyph.unicode = -1
            upright.selection.select(pname)
            upright.copy()
            latinfont.createChar(-1, pname)
            latinfont.selection.select(pname)
            latinfont.paste()

            rtl = latinfont.createChar(-1, name + ".rtl" + ".prop")
            rtl.addReference(pname, italic)
            rtl.useRefsMetrics(pname)

    # copy kerning classes
    fea = ""
    if not quran:
        for lookup in latinfont.gpos_lookups:
            fea += generateFeatureString(latinfont, lookup)

    for lookup in latinfont.gpos_lookups + latinfont.gsub_lookups:
        latinfont.removeLookup(lookup)

    latinfont.save(tmpfont)
    latinfont.close()

    font.mergeFonts(tmpfont)
    os.remove(tmpfont)

    # This is often used for visible space, so they better be the same width.
    if "periodcentered" in font:
        font["periodcentered"].width = font["space"].width
        centerGlyph(font["periodcentered"])

    # add Latin small and medium digits
    for name in digits:
        if italic:
            # they are only used in Arabic contexts, so always reference the
            # italic rtl variant
            refname = name +".rtl"
        else:
            refname = name
        small = font.createChar(-1, name + ".small")
        if not small.isWorthOutputting():
            small.clear()
            small.addReference(refname, psMat.scale(0.6))
            small.transform(psMat.translate(0, -40))
            small.width = 600
            centerGlyph(small)

        medium = font.createChar(-1, name + ".medium")
        if not medium.isWorthOutputting():
            medium.clear()
            medium.addReference(refname, psMat.scale(0.8))
            medium.transform(psMat.translate(0, 50))
            medium.width = 900
            centerGlyph(medium)

    return fea

def makeSlanted(options):
    font = makeDesktop(options, False)

    # compute amout of skew, magic formula copied from fontforge sources
    import math
    skew = psMat.skew(-options.slant * math.pi/180.0)

    # Remove Arabic math alphanumerics, they are upright-only.
    font.selection.select(["ranges"], "u1EE00", "u1EEFF")
    for glyph in font.selection.byGlyphs:
        font.removeGlyph(glyph)

    font.selection.all()
    punct = ("exclam", "period", "guillemotleft", "guillemotright",
             "braceleft", "bar", "braceright", "bracketleft", "bracketright",
             "parenleft", "parenright", "slash", "backslash", "brokenbar",
             "uni061F", "dot.1", "dot.2")

    for name in punct:
        font.selection.select(["less"], name)

    font.transform(skew)

    # fix metadata
    font.italicangle = options.slant
    font.fullname += " Slanted"
    if font.weight == "Bold":
        font.fontname = font.fontname.replace("Bold", "BoldSlanted")
        font.appendSFNTName("English (US)",   "SubFamily", "Bold Slanted")
    else:
        font.fontname = font.fontname.replace("Regular", "Slanted")

    fea = mergeLatin(font, italic=skew)
    makeNumerators(font)
    generateFont(options, font, fea)

def scaleGlyph(glyph, amount):
    """Scales the glyph, but keeps it centered around its original bounding
    box.

    Logic copied (and simplified for our simple case) from code of FontForge
    transform dialog, since that logic is not exported to Python interface."""
    width = glyph.width
    bbox = glyph.boundingBox()
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    move = psMat.translate(-x, -y)
    scale = psMat.scale(amount)

    matrix = list(scale)
    matrix[4] = move[4] * scale[0] + x;
    matrix[5] = move[5] * scale[3] + y;

    glyph.transform(matrix)
    if width == 0:
        glyph.width = width

def makeQuran(options):
    font = makeDesktop(options, False)

    # fix metadata
    font.fontname = font.fontname.replace("-Regular", "Quran-Regular")
    font.familyname += " Quran"
    font.fullname += " Quran"

    sample = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِیمِ ۝١ ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِینَ ۝٢"
    font.appendSFNTName('English (US)', 'Sample Text', sample)

    digits = ("zero", "one", "two", "three", "four", "five", "six",
              "seven", "eight", "nine")

    fea = mergeLatin(font, glyphs=digits, quran=True)

    for glyph in font.glyphs():
        if glyph.glyphname.endswith(".ara"):
            glyph.glyphname = glyph.glyphname[:-4]
            glyph.unicode = fontforge.unicodeFromName(glyph.glyphname)

    # scale some vowel marks and dots down a bit
    scaleGlyph(font["uni0651"], 0.8)
    for mark in ("uni064B", "uni064C", "uni064E", "uni064F", "uni06E1",
                 "uni08F0", "uni08F1", "uni08F2",
                 "TwoDots.a", "ThreeDots.a", "vTwoDots.a"):
        scaleGlyph(font[mark], 0.9)

    # create overline glyph to be used for sajda line, it is positioned
    # vertically at the level of the base of waqf marks
    fea += makeQuranSajdaLine(font, font[0x06D7].boundingBox()[1])

    unicodes = [font[n].unicode for n in digits]
    unicodes += ['.', '(', ')', '[', ']', '{', '}', '|', ' ', '/', '\\',
                 0x00AB, 0x00BB, 0x0305, 0x030A, 0x0325, 0x060C, 0x0615,
                 0x0617, 0x0618, 0x0619, 0x061A, 0x061B, 0x061E, 0x061F,
                 0x0621, 0x0622, 0x0623, 0x0624, 0x0625, 0x0626, 0x0627,
                 0x0628, 0x0629, 0x062A, 0x062B, 0x062C, 0x062D, 0x062E,
                 0x062F, 0x0630, 0x0631, 0x0632, 0x0633, 0x0634, 0x0635,
                 0x0636, 0x0637, 0x0638, 0x0639, 0x063A, 0x0640, 0x0641,
                 0x0642, 0x0643, 0x0644, 0x0645, 0x0646, 0x0647, 0x0648,
                 0x0649, 0x064A, 0x064B, 0x064C, 0x064D, 0x064E, 0x064F,
                 0x0650, 0x0651, 0x0652, 0x0653, 0x0654, 0x0655, 0x0656,
                 0x0657, 0x0658, 0x065C, 0x0660, 0x0661, 0x0662, 0x0663,
                 0x0664, 0x0665, 0x0666, 0x0667, 0x0668, 0x0669, 0x066E,
                 0x066F, 0x0670, 0x0671, 0x067A, 0x06A1, 0x06BA, 0x06CC,
                 0x06D6, 0x06D7, 0x06D8, 0x06D9, 0x06DA, 0x06DB, 0x06DC,
                 0x06DD, 0x06DE, 0x06DF, 0x06E0, 0x06E1, 0x06E2, 0x06E3,
                 0x06E4, 0x06E5, 0x06E6, 0x06E7, 0x06E8, 0x06E9, 0x06EA,
                 0x06EB, 0x06EC, 0x06ED, 0x06F0, 0x06F1, 0x06F2, 0x06F3,
                 0x06F4, 0x06F5, 0x06F6, 0x06F7, 0x06F8, 0x06F9, 0x08F0,
                 0x08F1, 0x08F2, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004,
                 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B,
                 0x200C, 0x200D, 0x200E, 0x200F, 0x2028, 0x2029, 0x202A,
                 0x202B, 0x202C, 0x202D, 0x202E, 0x202F, 0x25CC, 0xFD3E,
                 0xFD3F, 0xFDFA, 0xFDFD]
    unicodes = [isinstance(u, str) and ord(u) or u for u in unicodes]

    generateFont(options, font, fea)
    subsetFontFT(options.output, unicodes, quran=True)

def makeDesktop(options, generate=True):
    font = fontforge.open(options.input)
    font.encoding = "UnicodeFull" # avoid a crash if compact was set

    # remove anchors that are not needed in the production font
    cleanAnchors(font)

    # sample text to be used by font viewers
    sample = 'صِفْ خَلْقَ خَوْدٍ كَمِثْلِ ٱلشَّمْسِ إِذْ بَزَغَتْ يَحْظَىٰ ٱلضَّجِيعُ بِهَا نَجْلَاءَ مِعْطَارِ.'

    font.appendSFNTName('English (US)', 'Sample Text', sample)

    if generate:
        fea = mergeLatin(font)
        makeNumerators(font)
        generateFont(options, font, fea)
    else:
        return font

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build Amiri fonts.")
    parser.add_argument("--input", metavar="FILE", required=True, help="input font to process")
    parser.add_argument("--output", metavar="FILE", required=True, help="ouput font to write")
    parser.add_argument("--features", metavar="FILE", required=True, help="feature file to include")
    parser.add_argument("--version", type=float, required=True, help="font version")
    parser.add_argument("--slant", type=float, required=False, help="font slant")
    parser.add_argument("--quran", action='store_true', required=False, help="build Quran variant")

    args = parser.parse_args()

    if args.slant:
        makeSlanted(args)
    elif args.quran:
        makeQuran(args)
    else:
        makeDesktop(args)
