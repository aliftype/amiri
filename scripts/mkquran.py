import argparse
import re

from fontTools.ttLib import TTFont
from fontTools import subset

LAYER = re.compile('.*\.l\d+$')

def rename(font):
    names = set()
    for layers in font["COLR"].ColorLayers.values():
        names |= {l.name for l in layers if LAYER.match(l.name)}

    del font["COLR"]
    del font["CPAL"]

    glyphs = set(font.glyphOrder) - names
    options = subset.Options()
    options.set(layout_features='*', name_IDs='*', name_languages='*',
        notdef_outline=True, glyph_names=True)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(glyphs=glyphs)
    subsetter.subset(font)

    for name in font["name"].names:
        if name.nameID in (1, 3, 4, 6):
            string = name.toUnicode()
            if name.nameID in (3, 6):
                string = string.replace("QuranColored", "Quran")
            else:
                string = string.replace("Quran Colored", "Quran")

            name.string = string.encode(name.getEncoding())


def main():
    parser = argparse.ArgumentParser(description="Create a version of Amiri with colored marks using COLR/CPAL tables.")
    parser.add_argument("infile", metavar="INFILE", type=str, help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", type=str, help="output font to write")

    args = parser.parse_args()

    font = TTFont(args.infile, recalcTimestamp=False)

    rename(font)

    font.save(args.outfile)

if __name__ == "__main__":
    main()
