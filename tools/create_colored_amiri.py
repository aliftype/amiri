import argparse
import sys

from fontTools import ttLib

_LAYER2_GLYPHS = ("uni0618", "uni0619", "uni061A", "uni064B", "uni064C",
                  "uni064D", "uni064E", "uni064F", "uni0650", "uni0651",
                  "uni0652", "uni0657", "uni0658", "uni06E1", "uni08F0",
                  "uni08F1", "uni08F2",
                  "uni064B.small", "uni064E.small", "uni08F1.small",
                  "uni064F.small", "uni08F0.small", "uni064C.small",
                  "uni0657.small", "uni0650.small", "uni064D.small",
                  "uni0652.small2", "uni0650.small2", "uni064E.small2",
                  "uni0657.urd")
_LAYER3_GLYPHS = ("uni0615", "uni0617", "uni065C", "uni0670", "uni06D6",
                  "uni06D7", "uni06D8", "uni06D9", "uni06DA", "uni06DB",
                  "uni06DC", "uni06DD", "uni06DE", "uni06DF", "uni06E0",
                  "uni06E2", "uni06E3", "uni06E4", "uni06E5", "uni06E6",
                  "uni06E7", "uni06E8", "uni06E9", "uni06EA", "uni06EB",
                  "uni06EC", "uni06ED", "uni0670.isol", "uni0670.medi",
                  "uni06E5.medi", "uni06E6.medi")

_LAYERS = {"diacritics": _LAYER2_GLYPHS,
           "quranic-signs": _LAYER3_GLYPHS}

def process(infile, outfile):
    font = ttLib.TTFont(infile)
    font["COLR"] = ttLib.newTable("COLR")
    font["CPAL"] = ttLib.newTable("CPAL")

    COLR = ttLib.getTableModule("COLR")
    CPAL = ttLib.getTableModule("CPAL")

    colors = {}
    colors["diacritics"]    = CPAL.Color(red=0xff, green=0x00, blue=0x00, alpha=0xff) # red
    colors["quranic-signs"] = CPAL.Color(red=0x80, green=0x00, blue=0x80, alpha=0xff) # purple

    palette = colors.values()
    font["CPAL"].version = 0
    font["CPAL"].palettes = [palette]
    font["CPAL"].numPaletteEntries = len(palette)

    font["COLR"].version = 0
    font["COLR"].ColorLayers = {}

    for color in _LAYERS:
        glyphs = _LAYERS[color]
        color = colors[color]
        for glyph in glyphs:
            layer = COLR.LayerRecord(name=glyph, colorID=palette.index(color))
            font["COLR"][glyph] = [layer]

    font.save(outfile)

def main():
    parser = argparse.ArgumentParser(description="Create a version of Amiri with colored marks using COLR/CPAL tables.")
    parser.add_argument("infile", metavar="INFILE", type=str, help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", type=str, help="output font to write")

    args = parser.parse_args()

    process(args.infile, args.outfile)

if __name__ == "__main__":
    main()
