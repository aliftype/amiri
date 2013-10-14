#!/usr/bin/env python
import sys
import subprocess
import fontforge
import psMat
import unicodedata as ucd

def runHB(text, font):
    args = ['hb-shape',
            '--no-clusters',
            '--direction=rtl',
            '--script=arab',
            '--language=ar',
            '--features=+ss01', # for U+FDFC
            '--font-file=%s' %font,
            '--text=%s'      %text]

    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = process.communicate()[0]
    lines = []
    for line in out.split('\n'):
        glyphs = line.strip().strip('[]').split('|')
        new_glyphs = []

        for glyph in glyphs:
            x_advance = 0
            y_advance = 0
            x_offset = 0
            y_offset = 0

            if '@' in glyph:
                name, pos = glyph.split('@')
                if '+' in pos:
                    pos, adv = pos.split('+')
                    x_advance, y_advance = (',' in adv) and adv.split(',') or (adv, 0)
                x_offset, y_offset = (',' in pos) and pos.split(',') or (pos, 0)
            elif '+' in glyph:
                name, pos = glyph.split('+')
                x_advance, y_advance = (',' in pos) and pos.split(',') or (pos, 0)
            else:
                name = glyph

            new_glyphs.append([name, int(x_advance or 0), int(y_advance or 0), int(x_offset or 0), int(y_offset or 0)])
        lines.append(new_glyphs)

    return lines

def buildCompatChars(font, hbfont):
    zwj = u'\u200D'
    ranges = (
            (0xfb50, 0xfbb1),
            (0xfbd3, 0xfd3d),
            (0xfd50, 0xfdf9),
            (0xfdfc, 0xfdfc),
            (0xfe70, 0xfefc),
            )
    text = u''
    codes = []
    for r in ranges:
        for c in range(r[0], r[1]+1):
            dec = ucd.decomposition(unichr(c)).split()
            if dec:
                codes.append(c)
                keyword = dec[0]
                new_text = u''

                for i in dec[1:]:
                    new_text += unichr(int(str(i),16))

                if keyword == '<initial>':
                    new_text = new_text + zwj
                elif keyword == '<final>':
                    new_text = zwj + new_text
                elif keyword == '<medial>':
                    new_text = zwj + new_text + zwj

                text += new_text + '\n'

    lines = runHB(text, hbfont)
    i = 0
    for c in codes:
        components = lines[i]
        i += 1
        if components:
            glyph = font.createChar(c)
            glyph.clear()
            glyph.color = 0xff0000 # red color
            x = 0
            for component in components:
                name = component[0]
                x_advance = component[1]
                y_advance = component[2]
                x_offset = component[3]
                y_offset = component[4]

                matrix = psMat.translate(x + x_offset, y_offset)

                # ignore blank glyphs, e.g. space or ZWJ
                if font[name].foreground or font[name].references:
                    glyph.addReference(name, matrix)

                x += x_advance

            glyph.width = x


if __name__ == '__main__':
    sfdfont = fontforge.open(sys.argv[1])
    hbfont = sys.argv[2]
    buildCompatChars(sfdfont, hbfont)
    sfdfont.save()
