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
    for filename in sys.argv[1:]:
        font = fontforge.open(filename)
        blanks = checkBlanks(font)

        if blanks:
            results.append([filename, blanks])

    if results:
        for result in results:
            print >> sys.stderr, "%s has the following suspicious blank glyphs:" % result[0]
            print >> sys.stderr, result[1]
        sys.exit(1)
