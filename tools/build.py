#!/usr/bin/python
import fontforge
import os
import sys

family = "amiri"
source = "sources"
flags  = ("opentype", "dummy-dsig", "round", "short-post")

def fake_marks(font):
    """We don't have vowel marks yet, so we fake some place holders so that
    vowelled text don't come broken. Making empty zero width glyphs would have
    been all what is needed, but fontconfig is smart enough to filter empty
    glyphs from the font, we we fool it by making non-empty glyphs and
    substitute them by an empty glyph with a GSUB table."""

    print "Faking vowel marks"

    #font.encoding = "UnicodeFull"
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

def main(style):
    style = style.lower()
    base = os.path.join(source, "%s-%s" %(family, style))
    if os.path.isfile("%s.sfd" % base):
        file = "%s.sfd" % base
    elif os.path.isdir("%s.sfdir" % base):
        file = "%s.sfdir" % base
    else:
        print "Font for style: '%s' not found" % style
        sys.exit(1)

    font = fontforge.open(file)

    fake_marks(font)

    print "Gnerating %s-%s.ttf" %(family, style)
    font.generate("%s-%s.ttf" %(family, style), flags=flags)

    font.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "No style specified"
        sys.exit(1)
