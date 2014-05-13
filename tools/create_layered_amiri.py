import argparse
import sys

from fontTools.ttLib import TTFont

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

_LAYER_NAMES = ("letters", "diacritics", "quranic-signs")

def process(infile, outfile, layer):
    font = TTFont(infile)
    glyf = font["glyf"]

    glyphNamesToKeep = []
    if layer == "letters":
        for glyphName in font.getGlyphNames():
            if glyphName not in _LAYER2_GLYPHS and glyphName not in _LAYER3_GLYPHS:
                glyphNamesToKeep.append(glyphName)
    elif layer == "diacritics":
        glyphNamesToKeep = _LAYER2_GLYPHS
    elif layer == "quranic-signs":
        glyphNamesToKeep = _LAYER3_GLYPHS

    for glyphName in font.getGlyphNames():
        if glyphName not in glyphNamesToKeep:
            glyph = glyf[glyphName]
            if glyphName in ("uni0670.medi", "uni06E5.medi", "uni06E6.medi") and layer == "letters":
                # We want to keep the kashida part of those glyphs.
                components = []
                for component in glyph.components:
                    if component.glyphName != glyphName.split(".")[0]:
                        components.append(component)
                glyph.components = components
            else:
                # This will cause FontTools not to output any outlines for that
                # glyph.
                glyph.numberOfContours = 0

    font.save(outfile)

def main():
    parser = argparse.ArgumentParser(description="Clear font glyphs based on their class.")
    parser.add_argument("infile", metavar="INFILE", type=str, help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", type=str, help="output font to write")
    parser.add_argument("--layer", type=str, help="which layer to build (letters, diacritics or quranic-signs)", required=True)

    args = parser.parse_args()

    if args.layer not in _LAYER_NAMES:
        print("Unknown layer name: %s" % args.layer)
        print("Possiple names are: %s" % str(_LAYER_NAMES))
        sys.exit(1)

    process(args.infile, args.outfile, args.layer)

if __name__ == "__main__":
    main()
