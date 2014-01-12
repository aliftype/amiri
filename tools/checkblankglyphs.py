import sys
from sortsmill import ffcompat as fontforge

def checkBlanks(font):
    blanks = []
    for glyph in font.glyphs():
        if glyph.width == font.em:
            if glyph.unicode not in (0x2001, 0x2003):
                if glyph.foreground.isEmpty() and len(glyph.references) == 0:
                    blanks.append(glyph.glyphname)
    return blanks


if __name__ == "__main__":
    results = []
    filename = sys.argv[1]
    font = fontforge.open(filename)
    blanks = checkBlanks(font)

    if blanks:
        print >> sys.stderr, "%s has the following suspicious blank glyphs:" % filename
        print >> sys.stderr, blanks
        sys.exit(1)
