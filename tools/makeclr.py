import argparse

from fontTools.ttLib import TTFont, getTableModule, newTable

Color = getTableModule("CPAL").Color

RED = Color(red=0xcc, green=0x33, blue=0x33, alpha=0xff)
YELLOW = Color(red=0xee, green=0x99, blue=0x33, alpha=0xff)
GREEN = Color(red=0x00, green=0xa5, blue=0x50, alpha=0xff)
BLUE = Color(red=0x33, green=0x66, blue=0x99, alpha=0xff)

HAMAZAT_GLYPHS = (
    "uni0621",
    "uni0654",
    "uni0655",
    "hamza.above",
)

MARKS_GLYPHS = (
    "uni0618",
    "uni0619",
    "uni061A",
    "uni064B",
    "uni064C",
    "uni064D",
    "uni064E",
    "uni064F",
    "uni0650",
    "uni0651",
    "uni0652",
    "uni0657",
    "uni0658",
    "uni065C",
    "uni0670",
    "uni06DC", # XXX: can be both a mark and a pause
    "uni06DF",
    "uni06E0",
    "uni06E1",
    "uni06E2",
    "uni06E3",
    "uni06E4",
    "uni06E5",
    "uni06E6",
    "uni06E7",
    "uni06E8",
    "uni06EA",
    "uni06EB",
    "uni06EC",
    "uni06ED",
    "uni08F0",
    "uni08F1",
    "uni08F2",
    "hamza.wasl",
    "Dot",
    "TwoDots",
    "vTwoDots",
    "ThreeDots",
)

PAUSES_GLYPHS = (
    "uni0615",
    "uni0617",
    "uni06D6",
    "uni06D7",
    "uni06D8",
    "uni06D9",
    "uni06DA",
    "uni06DB",
)

SIGNS_GLYPHS = (
    "uni0305",
    "uni0660",
    "uni0661",
    "uni0662",
    "uni0663",
    "uni0664",
    "uni0665",
    "uni0666",
    "uni0667",
    "uni0668",
    "uni0669",
    "uni06DD",
    "uni06DE",
    "uni06E9",
)

GROUPS = {
    MARKS_GLYPHS: RED,
    SIGNS_GLYPHS: GREEN,
    HAMAZAT_GLYPHS: YELLOW,
    PAUSES_GLYPHS: BLUE,
}

HASHES = {}

def newLayer(name, colorID):
    return getTableModule("COLR").LayerRecord(name=name, colorID=colorID)

def getGlyphColor(glyphName):
    for names, color in GROUPS.items():
        for name in names:
            if glyphName == name or glyphName.startswith(name + "."):
                return color

    return None

def colorize(font):
    COLR = newTable("COLR")
    CPAL = newTable("CPAL")
    hmtx = font["hmtx"]

    glyf = font.get("glyf", None)
    CFF  = font.get("CFF ", None)

    if glyf is None:
        assert False, "CFF is not supported"

    CPAL.version = 0
    COLR.version = 0

    palette = list(GROUPS.values())
    CPAL.palettes = [palette]
    CPAL.numPaletteEntries = len(palette)

    COLR.ColorLayers = {}

    glyphOrder = list(font.getGlyphOrder())
    for name in glyphOrder:
        glyph = glyf[name]

        layers = []
        if glyph.isComposite() and len(glyph.components) > 1:
            componentColors = [getGlyphColor(c.getComponentInfo()[0]) for c in glyph.components]
            if any(componentColors):
                for component in glyph.components:
                    componentName, trans = component.getComponentInfo()
                    componentColor = getGlyphColor(componentName)

                    if componentColor is None:
                        # Special palette index that means the glyph has no
                        # specified color and takes the text color.
                        componentColor = 0xFFFF
                    else:
                        componentColor = palette.index(componentColor)

                    # Unique identifier for each layer, so we can reuse
                    # identical layers and avoid needless duplication.
                    width = hmtx[name][0]
                    lsb = hmtx[componentName][1] + trans[4]
                    componentHash = hash((trans, width, lsb))

                    if componentName not in HASHES:
                        HASHES[componentName] = []

                    if componentHash not in HASHES[componentName]:
                        HASHES[componentName].append(componentHash)

                    index = HASHES[componentName].index(componentHash)
                    newName = "%s.l%s" % (componentName, index)

                    if newName not in font.glyphOrder:
                        font.glyphOrder.append(newName)

                        newGlyph = getTableModule("glyf").Glyph()
                        newGlyph.numberOfContours = -1
                        newGlyph.components = [component]
                        glyf.glyphs[newName] = newGlyph
                        assert(len(glyf.glyphs) == len(font.glyphOrder)), (name, newName)

                        hmtx.metrics[newName] = [width, lsb]
                    layers.append(newLayer(newName, componentColor))

        if not layers:
            color = getGlyphColor(name)
            if color is not None:
                layers = [newLayer(name, palette.index(color))]

        if layers:
            COLR[name] = layers

    font["COLR"] = COLR
    font["CPAL"] = CPAL

def rename(font):
    for name in font["name"].names:
        if name.nameID in (1, 3, 4, 6):
            string = name.toUnicode()
            if name.nameID in (3, 6):
                string = string.replace("Quran", "QuranColored")
            else:
                string = string.replace("Quran", "Quran Colored")

            name.string = string.encode(name.getEncoding())

def main():
    parser = argparse.ArgumentParser(description="Create a version of Amiri with colored marks using COLR/CPAL tables.")
    parser.add_argument("infile", metavar="INFILE", type=str, help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", type=str, help="output font to write")

    args = parser.parse_args()

    font = TTFont(args.infile, recalcTimestamp=False)

    colorize(font)
    rename(font)

    font.save(args.outfile)

if __name__ == "__main__":
    main()
