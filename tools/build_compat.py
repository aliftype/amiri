#!/usr/bin/env python
import sys
import fontforge
import psMat
import unicodedata as ucd

from gi.repository import HarfBuzz
from gi.repository import GLib

from fontTools.ttLib import TTFont

try:
    unicode
except NameError:
    unicode = str

def toUnicode(s, encoding='utf-8'):
    return s if isinstance(s, unicode) else s.decode(encoding)

def shape(text, font):
    text = toUnicode(text)
    buf = HarfBuzz.buffer_create()

    HarfBuzz.buffer_add_utf8(buf, text.encode('utf-8'), 0, -1)
    HarfBuzz.buffer_set_direction(buf, HarfBuzz.direction_t.RTL)
    HarfBuzz.buffer_set_script(buf, HarfBuzz.script_t.ARABIC)
    HarfBuzz.buffer_set_language(buf, HarfBuzz.language_from_string("ar"))

    HarfBuzz.shape(font, buf, [HarfBuzz.feature_from_string("+ss01")[1]])

    glyphs = HarfBuzz.buffer_get_glyph_infos(buf)
    positions = HarfBuzz.buffer_get_glyph_positions(buf)

    return [(g.codepoint, p.x_advance, p.x_offset, p.y_offset) for g, p in zip(glyphs, positions)]

def buildCompatChars(sfd, ttf):
    zwj = u'\u200D'
    ranges = (
            (0xfb50, 0xfbb1),
            (0xfbd3, 0xfd3d),
            (0xfd50, 0xfdf9),
            (0xfdfc, 0xfdfc),
            (0xfe70, 0xfefc),
            )

    with open(ttf, "rb") as f:
        data = f.read()
        blob = HarfBuzz.glib_blob_create(GLib.Bytes.new(data))
        face = HarfBuzz.face_create(blob, 0)
        hbfont = HarfBuzz.font_create(face)
        upem = HarfBuzz.face_get_upem(face)
        HarfBuzz.font_set_scale(hbfont, upem, upem)
        HarfBuzz.ot_font_set_funcs(hbfont)

    ttfont = TTFont(ttf)

    for r in ranges:
        for c in range(r[0], r[1]+1):
            dec = ucd.decomposition(unichr(c)).split()
            if dec:
                keyword = dec[0]
                text = u''

                for i in dec[1:]:
                    text += unichr(int(str(i),16))

                if keyword == '<initial>':
                    text = text + zwj
                elif keyword == '<final>':
                    text = zwj + text
                elif keyword == '<medial>':
                    text = zwj + text + zwj

                components = shape(text, hbfont)
                if components:
                    glyph = sfd.createChar(c)
                    glyph.clear()
                    glyph.color = 0xff0000 # red color
                    x = 0
                    for component in components:
                        gid = component[0]
                        name = ttfont.getGlyphName(gid)
                        x_advance = component[1]
                        x_offset = component[2]
                        y_offset = component[3]

                        matrix = psMat.translate(x + x_offset, y_offset)

                        # ignore blank glyphs, e.g. space or ZWJ
                        if sfd[name].foreground or sfd[name].references:
                            glyph.addReference(name, matrix)

                        x += x_advance

                    glyph.width = x


if __name__ == '__main__':
    sfd = fontforge.open(sys.argv[1])
    ttf = sys.argv[2]

    buildCompatChars(sfd, ttf)
    sfd.save()
