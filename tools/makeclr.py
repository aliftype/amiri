import argparse

from fontTools.ttLib import TTFont, getTableModule, newTable

MARKS = getTableModule("CPAL").Color(red=0x00, green=0x80, blue=0x00, alpha=0xff) # green
SIGNS = getTableModule("CPAL").Color(red=0x80, green=0x00, blue=0x80, alpha=0xff) # purple
BLACK = getTableModule("CPAL").Color(red=0x00, green=0x00, blue=0x00, alpha=0xff)

MARKS_GLYPHS = (
    "uni0618", "uni0619", "uni061A", "uni064B", "uni064C",
    "uni064D", "uni064E", "uni064F", "uni0650", "uni0651",
    "uni0652", "uni0657", "uni0658", "uni06E1", "uni08F0",
    "uni08F1", "uni08F2", "uni0657.urd",
    "uni064B.small", "uni064E.small", "uni08F1.small",
    "uni064F.small", "uni08F0.small", "uni064C.small",
    "uni0657.small", "uni0650.small", "uni064D.small",
    "uni0652.small2", "uni0650.small2", "uni064E.small2",
)
SIGNS_GLYPHS = (
    "uni0615", "uni0617", "uni065C", "uni0670", "uni06D6",
    "uni06D7", "uni06D8", "uni06D9", "uni06DA", "uni06DB",
    "uni06DC", "uni06DD", "uni06DE", "uni06DF", "uni06E0",
    "uni06E2", "uni06E3", "uni06E4", "uni06E5", "uni06E6",
    "uni06E7", "uni06E8", "uni06E9", "uni06EA", "uni06EB",
    "uni06EC", "uni06ED", "uni0670.isol", "uni0670.medi",
    "uni06E5.medi", "uni06E6.medi", "uni06E5.low"
)

GROUPS = {
    MARKS: MARKS_GLYPHS,
    SIGNS: SIGNS_GLYPHS,
    BLACK: [],
}

def newLayer(name, colorID):
    return getTableModule("COLR").LayerRecord(name=name, colorID=colorID)

def colorize(font):
    COLR = newTable("COLR")
    CPAL = newTable("CPAL")
    glyf = font["glyf"]
    hmtx = font["hmtx"]

    CPAL.version = 0
    COLR.version = 0

    palette = list(GROUPS.keys())
    CPAL.palettes = [palette]
    CPAL.numPaletteEntries = len(palette)

    COLR.ColorLayers = {}

    for color in GROUPS:
        names = GROUPS[color]
        for name in names:
            layers = []
            if name.endswith(".medi"):
                glyph = glyf[name]
                assert(glyph.isComposite())
                for component in glyph.components:
                    componentName, trans = component.getComponentInfo()
                    if trans == (1, 0, 0, 1, 0, 0):
                        # broken in current versions of Firefox,
                        # see https://bugzilla.mozilla.org/show_bug.cgi?id=1283932
                       #layers.append(newLayer(componentName, 0xFFFF)) # broken if FF47
                        layers.append(newLayer(componentName, palette.index(BLACK)))
                    else:
                        newName = "%s.%s" % (name, componentName)
                        font.glyphOrder.append(newName)

                        newGlyph = getTableModule("glyf").Glyph()
                        newGlyph.numberOfContours = -1
                        newGlyph.components = [component]
                        glyf.glyphs[newName] = newGlyph

                        width = hmtx[name][0]
                        lsb = hmtx[componentName][1] + trans[4]
                        hmtx.metrics[newName] = [width, lsb]

                        layers.append(newLayer(newName, palette.index(color)))
            else:
                layers.append(newLayer(name, palette.index(color)))
            COLR[name] = layers

    font["COLR"] = COLR
    font["CPAL"] = CPAL

def rename(font):
    name = font["name"]
    for record in name.names:
        nameID = record.nameID
        platID = record.platformID
        langID = record.langID
        encoID = record.platEncID

        encoding = "latin1"
        if record.isUnicode():
            encoding = 'utf_16_be'

        if nameID in (1, 4, 6):
            string = record.string.decode(encoding)
            if nameID == 6:
                if "-" in string:
                    family, subfamily = string.split("-")
                    string = "%sColored-%s" % (family, subfamily)
                else:
                    string += "Colored"
            else:
                string += " Colored"

            record.string = string.encode(encoding)

def main():
    parser = argparse.ArgumentParser(description="Create a version of Amiri with colored marks using COLR/CPAL tables.")
    parser.add_argument("infile", metavar="INFILE", type=str, help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", type=str, help="output font to write")

    args = parser.parse_args()

    font = TTFont(args.infile)

    colorize(font)
    rename(font)

    font.save(args.outfile)

if __name__ == "__main__":
    main()
