import argparse
import os

from fontTools.ttLib import TTFont
from sortsmill import ffcompat as fontforge
from tempfile import mkstemp

def makeWeb(infile, outfile):
    """If we are building a web version then try to minimise file size"""

    # "short-post" generates a post table without glyph names to save some KBs
    # since glyph names are only needed for PDF's as readers use them to
    # "guess" characters when copying text, which is of little use in web fonts.
    flags = ("opentype", "short-post", "omit-instructions")

    fontforge.setPrefs("PreserveTables", "COLR,CPAL")

    font = fontforge.open(infile)
    font.encoding = "UnicodeBmp" # avoid a crash if compact was set

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

    tmpfile = mkstemp(suffix=os.path.basename(outfile))[1]
    font.generate(tmpfile, flags=flags)
    font.close()

    # now open in fontTools
    from fontTools.ttLib import TTFont
    ftfont = TTFont(tmpfile)

    # force compiling tables by fontTools, saves few tens of KBs
    for tag in ftfont.keys():
        if hasattr(ftfont[tag], "compile"):
            ftfont[tag].compile(ftfont)

    ftfont.save(outfile)
    ftfont.close()

    os.remove(tmpfile)


def main():
    parser = argparse.ArgumentParser(description="Create web optimised version of Amiri fonts.")
    parser.add_argument("infile", metavar="INFILE", help="input font to process")
    parser.add_argument("outfile", metavar="OUTFILE", help="output font to write")

    args = parser.parse_args()

    makeWeb(args.infile, args.outfile)

if __name__ == "__main__":
    main()
