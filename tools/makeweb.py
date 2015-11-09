import argparse
import os

from fontTools.ttLib import TTFont
from fontTools import subset

def makeWeb(infile, outfile):
    """If we are building a web version then try to minimise file size"""

    font = TTFont(infile)

    # removed compatibility glyphs that of little use on the web
    ranges = (
            (0xfb50, 0xfbb1),
            (0xfbd3, 0xfd3d),
            (0xfd50, 0xfdf9),
            (0xfdfc, 0xfdfc),
            (0xfe70, 0xfefc),
            )

    cmap = font['cmap'].buildReversed()
    unicodes = set([min(cmap[c]) for c in cmap])
    for r in ranges:
        unicodes -= set(range(r[0], r[1] + 1))

    options = subset.Options()
    options.set(layout_features='*', name_IDs='*', drop_tables=['DSIG'])
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    font.save(outfile)
    font.close()


def main():
    parser = argparse.ArgumentParser(description="Create web optimised version of Amiri fonts.")
    parser.add_argument("infile", metavar="INFILE", help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", help="output font to write")

    args = parser.parse_args()

    makeWeb(args.infile, args.outfile)

if __name__ == "__main__":
    main()
