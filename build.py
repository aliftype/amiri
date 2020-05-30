#!/usr/bin/env python
# coding=utf-8
#
# build.py - Amiri font build utility
#
# Copyright 2010-2019 Khaled Hosny <khaledhosny@eglug.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from io import StringIO
from pcpp.preprocessor import Preprocessor

from sfdLib.parser import SFDParser
from sfdLib.utils import sortGlyphs
from ufo2ft import compileOTF, compileTTF

from ufo2ft.filters.transformations import TransformationsFilter
from fontTools.feaLib import ast


def cleanAnchors(font):
    """Removes anchor classes (and associated lookups) that are used only
    internally for building composite glyph."""

    lookups = (
            "markDash",
           #"markDigitAbove",
            "markDigitBelow",
            "markDotAbove",
            "markDotAlt",
            "markDotBelow",
            "markDotBelowAlt",
            "markDotHmaza",
            "markMarkDotAbove",
            "markMarkDotBelow",
            "markRingBelow",
            "markRingDash",
            "markStroke",
           #"markTaaAbove",
            "markTaaBelow",
            "markTail",
            "markTashkilAboveDot",
            "markTashkilBelowDot",
            "markTwoDotsAbove",
            "markTwoDotsBelow",
            "markTwoDotsBelowAlt",
            "markVAbove",
            )

    def keep(s):
        if isinstance(s, ast.LookupBlock) and s.name in lookups:
            return False
        if isinstance(s, ast.LookupReferenceStatement) and s.lookup.name in lookups:
            return False
        return True

    fea = font.features.text = parseFea(font.features.text)
    fea.statements = [s for s in fea.statements if  keep(s)]
    for block in fea.statements:
        if hasattr(block, "statements"):
            block.statements = [s for s in block.statements if keep(s)]


def generateFeatures(font, args):
    """Generates feature text by merging feature file with mark positioning
    lookups (already in the font) and making sure they come after kerning
    lookups (from the feature file), which is required by Uniscribe to get
    correct mark positioning for kerned glyphs."""

    # open feature file and insert the generated GPOS features in place of the
    # placeholder text
    preprocessor = Preprocessor()
    if args.quran:
        preprocessor.define("QURAN")
    elif args.slant:
        preprocessor.define("ITALIC")
    with open(args.features) as f:
        preprocessor.parse(f)
    o = StringIO()
    preprocessor.write(o)
    fea = o.getvalue()
    font.features.text = fea.replace("#{%anchors%}", font.features.text.asFea())


def generateFont(options, font):
    generateFeatures(font, options)

    from datetime import datetime
    info = font.info
    major, minor = options.version.split(".")
    info.versionMajor, info.versionMinor = int(major), int(minor)
    year = datetime.now().year
    info.copyright = f"Copyright 2010-{year} The Amiri Project Authors (https://github.com/alif-type/amiri)."
    info.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://scripts.sil.org/OFL"
    info.openTypeNameLicenseURL = "https://scripts.sil.org/OFL"

    if options.output.endswith(".ttf"):
        from fontTools.ttLib import newTable
        from fontTools.ttLib.tables import ttProgram
        otf = compileTTF(font, inplace=True, removeOverlaps=True,
            overlapsBackend="pathops", featureWriters=[])

        otf["DSIG"] = DSIG = newTable("DSIG")
        DSIG.ulVersion = 1
        DSIG.usFlag = 0
        DSIG.usNumSigs = 0
        DSIG.signatureRecords = []

        otf["prep"] = prep = newTable("prep")
        prep.program = ttProgram.Program()
        prep.program.fromAssembly([
            'PUSHW[]', '511', 'SCANCTRL[]', 'PUSHB[]', '4', 'SCANTYPE[]'])
    else:
        import cffsubr
        otf = compileOTF(font, inplace=True, optimizeCFF=0, removeOverlaps=True,
            overlapsBackend="pathops", featureWriters=[])
        cffsubr.subroutinize(otf)

    if info.styleMapStyleName and "italic" in info.styleMapStyleName:
        otf['name'].names = [n for n in otf['name'].names if n.nameID != 17]
        for name in otf['name'].names:
            if name.nameID == 2:
                name.string = info.styleName
    glyf = otf.get("glyf")
    if glyf:
        from fontTools.ttLib.tables._g_l_y_f import UNSCALED_COMPONENT_OFFSET
        for name, glyph in glyf.glyphs.items():
            glyph.expand(glyf)
            if glyph.isComposite():
                for component in glyph.components:
                    component.flags |= UNSCALED_COMPONENT_OFFSET

    return otf


def drawOverline(font, name, uni, pos, thickness, width):
    try:
        glyph = font[name]
    except KeyError:
        glyph = font.newGlyph(name)
        glyph.width = 0

    pen = glyph.getPen()

    pen.moveTo((-50, pos))
    pen.lineTo((-50, pos + thickness))
    pen.lineTo((width + 50, pos + thickness))
    pen.lineTo((width + 50, pos))
    pen.closePath()

    return glyph


def makeQuranSajdaLine(font):
    pos = font["uni06D7"].getBounds(font).yMax
    thickness = font.info.postscriptUnderlineThickness
    minwidth = 100


    _, gdefclasses = findGDEF(font)
    # collect glyphs grouped by their widths rounded by 100 units, we will use
    # them to decide the widths of over/underline glyphs we will draw
    widths = {}
    for glyph in font:
        u = glyph.unicode
        if ((u is None ) or (0x0600 <= u <= 0x06FF) or u == ord(" ")) \
        and glyph.width > 0:
            width = round(glyph.width / minwidth) * minwidth
            width = width > minwidth and width or minwidth
            if not width in widths:
                widths[width] = []
            widths[width].append(glyph.name)

    base = 'uni0305'
    drawOverline(font, base, 0x0305, pos, thickness, 500)

    mark = ast.FeatureBlock("mark")
    overset = ast.GlyphClassDefinition("OverSet", ast.GlyphClass([base]))
    lookupflag = ast.LookupFlagStatement(markFilteringSet=ast.GlyphClassName(overset))
    mark.statements.extend([overset, lookupflag])

    for width in sorted(widths.keys()):
        # for each width group we create an over/underline glyph with the same
        # width, and add a contextual substitution lookup to use it when an
        # over/underline follows any glyph in this group
        replace = f"uni0305.{width}"
        drawOverline(font, replace, None, pos, thickness, width)
        sub = ast.SingleSubstStatement([ast.GlyphName(base)],
                                       [ast.GlyphName(replace)],
                                       [ast.GlyphClass(widths[width])],
                                       [], False)
        gdefclasses.markGlyphs.append(replace)
        mark.statements.append(sub)

    font.features.text.statements.append(mark)


def subsetFont(otf, unicodes):
    from fontTools import subset

    options = subset.Options()
    options.set(layout_features='*', name_IDs='*', name_languages='*',
        notdef_outline=True, glyph_names=True)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(otf)
    return otf


def parseFea(text):
    from fontTools.feaLib.parser import Parser

    if isinstance(text, ast.FeatureFile):
        return text
    f = StringIO(text)
    fea = Parser(f).parse()
    return fea


def findGDEF(font):
    fea = font.features.text = parseFea(font.features.text)
    gdef = None
    classes = None
    for block in fea.statements:
        if isinstance(block, ast.TableBlock) and block.name == "GDEF":
            gdef = block
            for statement in block.statements:
                if isinstance(statement, ast.GlyphClassDefStatement):
                    classes = statement
                    break
            break

    return gdef, classes


def mergeLatin(font):
    fontname = font.info.postscriptFontName.replace("Amiri", "AmiriLatin")
    latin = openFont("sources/latin/%s.sfd" % fontname)
    for glyph in latin:
        try:
            font.addGlyph(glyph)
        except KeyError:
            pass

    # Merge features
    gdef, classes = findGDEF(font)
    fea = font.features.text
    latinfea = parseFea(latin.features.text)
    for block in latinfea.statements:
        if isinstance(block, ast.TableBlock) and block.name == "GDEF":
            for st in block.statements:
                if isinstance(st, ast.GlyphClassDefStatement):
                    classes.baseGlyphs.extend(st.baseGlyphs.glyphSet())
                    classes.componentGlyphs.extend(st.componentGlyphs.glyphSet())
                    classes.ligatureGlyphs.extend(st.ligatureGlyphs.glyphSet())
                    classes.markGlyphs.extend(st.markGlyphs.glyphSet())
                else:
                    gdef.statements.append(st)
        else:
            fea.statements.append(block)
    font.features.text = fea
    font.glyphOrder += latin.glyphOrder
    font.glyphOrder = sortGlyphs(font)


def transformAnchor(anchor, matrix):
    if not anchor:
        return anchor

    from fontTools.misc.fixedTools import otRound
    anchor.x, anchor.y = matrix.transformPoint((anchor.x, anchor.y))
    anchor.x = otRound(anchor.x)
    anchor.y = otRound(anchor.y)

    return anchor


def makeSlanted(options):
    font = makeDesktop(options, False)

    exclude = [f"u{i:X}" for i in range(0x1EE00, 0x1EEFF + 1)]
    exclude += [
        "exclam", "period.ara", "guillemotleft.ara", "guillemotright.ara",
        "braceleft", "bar", "braceright", "bracketleft", "bracketright",
        "parenleft", "parenright", "slash", "backslash", "brokenbar",
        "uni061F", "dot.1", "dot.2",
    ]

    skew = TransformationsFilter(Slant=-options.slant, exclude=exclude)
    skew(font)

    # fix metadata
    info = font.info
    info.italicAngle = options.slant
    info.postscriptFullName += " Slanted"
    if info.postscriptWeightName == "Bold":
        info.postscriptFontName = info.postscriptFontName.replace("Bold", "BoldSlanted")
        info.styleName = "Bold Slanted"
        info.styleMapFamilyName = info.familyName
        info.styleMapStyleName = "bold italic"
    else:
        info.postscriptFontName = info.postscriptFontName.replace("Regular", "Slanted")
        info.styleName = "Slanted"
        info.styleMapFamilyName = info.familyName
        info.styleMapStyleName = "italic"

    matrix = skew.context.matrix
    mergeLatin(font)
    fea = font.features.text
    for block in fea.statements:
        if isinstance(block, (ast.LookupBlock, ast.FeatureBlock)):
            for st in block.statements:
                if isinstance(st, (ast.MarkMarkPosStatement, ast.MarkBasePosStatement)):
                    st.marks = [(transformAnchor(a, matrix), m) for a, m in st.marks]
                elif isinstance(st, ast.MarkClassDefinition):
                    st.anchor = transformAnchor(st.anchor, matrix)
                elif isinstance(st, ast.CursivePosStatement):
                    st.entryAnchor = transformAnchor(st.entryAnchor, matrix)
                    st.exitAnchor = transformAnchor(st.exitAnchor, matrix)

    otf = generateFont(options, font)
    otf.save(options.output)


def scaleGlyph(font, glyph, scale):
    """Scales the glyph, but keeps it centered around its original bounding
    box."""
    from fontTools.pens.recordingPen import RecordingPointPen
    from fontTools.pens.transformPen import TransformPointPen
    from fontTools.misc.transform import Identity

    width = glyph.width
    bbox = glyph.getBounds(font)
    x = (bbox.xMin + bbox.xMax) / 2
    y = (bbox.yMin + bbox.yMax) / 2
    matrix = Identity
    matrix = matrix.translate(-x * scale + x, -y * scale + y)
    matrix = matrix.scale(scale)

    rec = RecordingPointPen()
    glyph.drawPoints(rec)
    glyph.clearContours()
    glyph.clearComponents()

    pen = TransformPointPen(glyph.getPointPen(), matrix)
    rec.replay(pen)

    if width == 0:
        glyph.width = width

    return matrix


def makeQuran(options):
    font = makeDesktop(options, False)
    mergeLatin(font)

    # fix metadata
    info = font.info
    info.postscriptFontName = info.postscriptFontName.replace("-Regular", "QuranColored-Regular")
    info.familyName += " Quran Colored"
    info.postscriptFullName += " Quran Colored"
    info.openTypeNameSampleText  = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ ۝١ ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَـٰلَمِینَ ۝٢"
    info.openTypeOS2TypoAscender = info.openTypeHheaAscender = 1815

    # scale some vowel marks and dots down a bit
    fea = font.features.text
    marks = [
        "uni064B", "uni064C", "uni064E", "uni064F", "uni06E1", "uni08F0",
        "uni08F1", "uni08F2", "TwoDots.a", "ThreeDots.a", "vTwoDots.a",
    ]
    shadda = ["uni0651"]
    for scale, names in ((0.9, marks), (0.8, shadda)):
        for name in names:
            matrix = scaleGlyph(font, font[name], scale)

            for block in fea.statements:
                for s in getattr(block, "statements", []):
                    if isinstance(s, ast.MarkClassDefinition) and name in s.glyphSet():
                        s.anchor = transformAnchor(s.anchor, matrix)
                    if isinstance(s, ast.MarkMarkPosStatement) and name in s.baseMarks.glyphSet():
                        s.marks = [(transformAnchor(a, matrix), m) for a, m in s.marks]

    # create overline glyph to be used for sajda line, it is positioned
    # vertically at the level of the base of waqf marks
    makeQuranSajdaLine(font)

    COLR, CPAL = makeCOLR(font)

    otf = generateFont(options, font)
    otf["COLR"] = COLR
    otf["CPAL"] = CPAL

    unicodes =  ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 '.', '(', ')', '[', ']', '{', '}', '|', ' ', '/', '\\',
                 0x00A0,
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
                 0x08F1, 0x08F2, 0x08F3, 0x2000, 0x2001, 0x2002, 0x2003,
                 0x2004,
                 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B,
                 0x200C, 0x200D, 0x200E, 0x200F, 0x2028, 0x2029, 0x202A,
                 0x202B, 0x202C, 0x202D, 0x202E, 0x202F, 0x25CC, 0xFD3E,
                 0xFD3F, 0xFDFA, 0xFDFD]
    unicodes = [isinstance(u, str) and ord(u) or u for u in unicodes]
    otf = subsetFont(otf, unicodes)
    otf.save(options.output)


def makeCOLR(font):
    from fontTools.ttLib import getTableModule, newTable
    from fontTools.misc.transform import Identity

    Color = getTableModule("CPAL").Color

    hamzas = ("uni0621", "uni0654", "uni0655", "hamza.above")
    marks = (
        "uni0618", "uni0619", "uni061A", "uni064B", "uni064C", "uni064D",
        "uni064E", "uni064F", "uni0650", "uni0651", "uni0652", "uni0657",
        "uni0658", "uni065C", "uni0670", "uni06DF", "uni06E0", "uni06E1",
        "uni06E2", "uni06E3", "uni06E4", "uni06E5", "uni06E6", "uni06E7",
        "uni06E8", "uni06EA", "uni06EB", "uni06EC", "uni06ED", "uni08F0",
        "uni08F1", "uni08F2", "uni08F3",
        "uni06DC", # XXX: can be both a mark and a pause
        "hamza.wasl", "Dot", "TwoDots", "vTwoDots", "ThreeDots",
    )

    pauses = (
        "uni0615", "uni0617", "uni06D6", "uni06D7", "uni06D8", "uni06D9",
        "uni06DA", "uni06DB",
    )

    signs = (
        "uni0305", "uni0660", "uni0661", "uni0662", "uni0663", "uni0664",
        "uni0665", "uni0666", "uni0667", "uni0668", "uni0669", "uni06DD",
        "uni06DE", "uni06E9",
    )

    groups = {
        marks: Color(red=0xcc, green=0x33, blue=0x33, alpha=0xff), # red
        signs: Color(red=0x00, green=0xa5, blue=0x50, alpha=0xff), # green
        hamzas: Color(red=0xee, green=0x99, blue=0x33, alpha=0xff), # yellow
        pauses: Color(red=0x33, green=0x66, blue=0x99, alpha=0xff), # blue
    }


    COLR = newTable("COLR")
    CPAL = newTable("CPAL")
    CPAL.version = 0
    COLR.version = 0

    palette = list(groups.values())
    CPAL.palettes = [palette]
    CPAL.numPaletteEntries = len(palette)

    COLR.ColorLayers = {}

    def newLayer(name, colorID):
        return getTableModule("COLR").LayerRecord(name=name, colorID=colorID)


    def getColor(glyphName):
        for names, color in groups.items():
            for name in names:
                if glyphName == name or glyphName.startswith(name + "."):
                    return palette.index(color)
        return 0xFFFF


    hashes = {}
    glyphOrder = list(font.glyphOrder)
    for name in glyphOrder:
        glyph = font[name]
        layers = []
        components = [(c, getColor(c.baseGlyph)) for c in glyph.components]
        if len(components) > 1 and any(c[1] != 0xFFFF for c in components):
            for component, color in components:
                componentName = component.baseGlyph
                trans = component.transformation
                if trans != Identity:
                    # Unique identifier for each layer, so we can reuse
                    # identical layers and avoid needless duplication.
                    componentHash = hash((trans, glyph.width))

                    if component.baseGlyph not in hashes:
                        hashes[componentName] = []

                    if componentHash not in hashes[componentName]:
                        hashes[componentName].append(componentHash)

                    index = hashes[componentName].index(componentHash)
                    componentName = f"{componentName}.l{index}"

                if componentName not in font:
                    newGlyph = font.newGlyph(componentName)
                    newGlyph.components = [component]
                    newGlyph.width = glyph.width
                layers.append(newLayer(componentName, color))

        if not layers:
            color = getColor(name)
            if color != 0xFFFF:
                layers = [newLayer(name, color)]

        if layers:
            COLR[name] = layers

    return COLR, CPAL


def openFont(path):
    from ufoLib2 import Font

    font = Font(validate=False)
    parser = SFDParser(path, font, ignore_uvs=False, ufo_anchors=False,
        ufo_kerning=False, minimal=True)
    parser.parse()

    return font


def makeDesktop(options, generate=True):
    font = openFont(options.input)

    # remove anchors that are not needed in the production font
    cleanAnchors(font)

    if generate:
        mergeLatin(font)
        otf = generateFont(options, font)
        otf.save(options.output)
    else:
        return font


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build Amiri fonts.")
    parser.add_argument("--input", metavar="FILE", required=True, help="input font to process")
    parser.add_argument("--output", metavar="FILE", required=True, help="ouput font to write")
    parser.add_argument("--features", metavar="FILE", required=True, help="feature file to include")
    parser.add_argument("--version", type=str, required=True, help="font version")
    parser.add_argument("--slant", type=float, required=False, help="font slant")
    parser.add_argument("--quran", action='store_true', required=False, help="build Quran variant")

    args = parser.parse_args()

    if args.slant:
        makeSlanted(args)
    elif args.quran:
        makeQuran(args)
    else:
        makeDesktop(args)
