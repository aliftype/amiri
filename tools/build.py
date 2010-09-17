#!/usr/bin/python
# encoding: utf-8
import fontforge
import sys
import os

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

def generate_css(font, out, base):
    if font.fullname.lower().find("slanted")>0:
        style = "slanted"
    else:
        style = "normal"

    weight = font.os2_weight
    family = "%sWeb" %font.familyname
    name = font.fontname

    begin = "/* begin %s */\n" %name
    end = "/* end %s */\n" %name

    inside = False
    css = ""
    if os.path.isfile(out):
        file = open(out, "r")

        for line in file.readlines():
            if line == begin:
                inside = True
            elif line == end:
                inside = False
            elif not inside:
                css += line

        file.close()

    css += begin
    css += """@font-face {
    font-style: %(style)s;
    font-weight: %(weight)s;
    font-family: "%(family)s";
    src: url('%(base)s.eot');
    src: local('☺'),
         url('%(base)s.woff') format('woff'),
         url('%(base)s.ttf') format('truetype');
}
""" %{"style":style, "weight":weight, "family":family, "base":base}
    css += end

    file = open(out, "w")
    file.write(css)
    file.close()

def main(sfd, out):
    css = False
    ext = os.path.splitext(out)[1].lower()
    base = os.path.splitext(os.path.basename(sfd))[0]
    if ext == ".css":
        css = True

    font = fontforge.open(sfd)

    if css:
        generate_css(font, out, base)
    else:
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
