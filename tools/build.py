#!/usr/bin/python
import fontforge
import sys

flags  = ("opentype", "dummy-dsig", "round", "short-post")

def fake_marks(font):
    """We don't have vowel marks yet, so we fake some place holders so that
    vowelled text don't come broken. Making empty zero width glyphs would have
    been all what is needed, but fontconfig is smart enough to filter empty
    glyphs from the font, we we fool it by making non-empty glyphs and
    substitute them by an empty glyph with a GSUB table."""

    font.addLookup("fake marks", "gsub_single", (),
            (("ccmp",(("arab",("dflt")),)),) )
    font.addLookupSubtable("fake marks", "fake marks-1")

    fake_mark = font.createChar(-1, "fake_mark")
    fake_mark.width = 0
    fake_mark.glyphclass = "mark"

    mark = 0x064B
    while mark <= 0x0652:
        glyph = font.createChar(mark)
        pen = glyph.glyphPen()
        pen.moveTo((100,100))
        pen.lineTo((100,200))
        pen.lineTo((200,200))
        pen.lineTo((200,100))
        pen.closePath()

        glyph.width = 0
        glyph.addPosSub("fake marks-1", "fake_mark")
        mark += 1

def main(sfd, out):
    font = fontforge.open(sfd)
    fake_marks(font)
    font.generate(out)
    font.close()

def usage():
    print "Usage: %s input_file output_file" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        usage()
        sys.exit(1)
