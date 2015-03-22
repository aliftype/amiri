#!/usr/bin/env python

import sys
import os
import csv

from gi.repository import HarfBuzz
from gi.repository import GLib

from fontTools.ttLib import TTFont

HbFonts = {}
def getHbFont(fontname):
    if fontname not in HbFonts:
        font = open(fontname, "rb")
        data = font.read()
        font.close()
        blob = HarfBuzz.glib_blob_create(GLib.Bytes.new(data))
        face = HarfBuzz.face_create(blob, 0)
        font = HarfBuzz.font_create(face)
        upem = HarfBuzz.face_get_upem(face)
        HarfBuzz.font_set_scale(font, upem, upem)
        HarfBuzz.ot_font_set_funcs(font)

        HbFonts[fontname] = font

    return HbFonts[fontname]

TtFonts = {}
def getTtFont(fontname):
    if fontname not in TtFonts:
        font = TTFont(fontname)
        TtFonts[fontname] = font

    return TtFonts[fontname]

HbLangs = {}
def getHbLang(name):
    if name not in HbLangs:
        lang = HarfBuzz.language_from_string(name)
        HbLangs[name] = lang

    return HbLangs[name]

HbFeats = {}
def getHbFeat(name):
    if name not in HbFeats:
        feat = HarfBuzz.feature_from_string(name)[1]
        HbFeats[name] = feat

    return HbFeats[name]

def toUnicode(s, encoding='utf-8'):
    if not isinstance(s, unicode):
        return s.decode(encoding)
    else:
        return s

def runHB(row, fontname, positions=False):
    direction, script, language, features, text = row[:5]
    font = getHbFont(fontname)
    buf = HarfBuzz.buffer_create()
    text = toUnicode(text)
    HarfBuzz.buffer_add_utf8(buf, text.encode('utf-8'), 0, -1)
    HarfBuzz.buffer_set_direction(buf, HarfBuzz.direction_from_string(direction))
    if script:
        HarfBuzz.buffer_set_script(buf, HarfBuzz.script_from_string(script))
    else:
        HarfBuzz.buffer_guess_segment_properties(buf)
    if language:
        HarfBuzz.buffer_set_language(buf, getHbLang(language))

    if features:
        features = [getHbFeat(fea) for fea in features.split(',')]
    else:
        features = []
    HarfBuzz.shape(font, buf, features)

    info = HarfBuzz.buffer_get_glyph_infos(buf)
    ttfont = getTtFont(fontname)
    if positions:
        pos = HarfBuzz.buffer_get_glyph_positions(buf)
        glyphs = []
        for i, p in zip(info, pos):
            glyph = ttfont.getGlyphName(i.codepoint)
            if p.x_offset or p.y_offset:
                glyph += "@%d,%d" % (p.x_offset, p.y_offset)
            glyph += "+%d" % p.x_advance
            if p.y_advance:
                glyph += ",%d" % p.y_advance
            glyphs.append(glyph)
        out = "|".join(glyphs)
    else:
        out = "|".join([ttfont.getGlyphName(i.codepoint) for i in info])

    return "[%s]" % out

def runTest(test, font, positions):
    count = 0
    failed = {}
    passed = []
    for row in test:
        count += 1
        row[4] = ('\\' in row[4]) and row[4].decode('unicode-escape') or row[4]
        text = row[4]
        reference = row[5]
        result = runHB(row, font, positions)
        if reference == result:
            passed.append(count)
        else:
            failed[count] = (text, reference, result)

    return passed, failed

def initTest(test, font, positions):
    out = ""
    for row in test:
        text = row[4]
        row[4] = ('\\' in row[4]) and row[4].decode('unicode-escape') or row[4]
        result = runHB(row, font, positions)
        out += "%s;%s;%s\n" %(";".join(row[:4]), text, result)

    return out

if __name__ == '__main__':
    init = False
    positions = False
    args = sys.argv[1:]

    if len (sys.argv) > 2 and sys.argv[1] == "-i":
        init = True
        args = sys.argv[2:]

    for arg in args:
        testname = arg

        ext = os.path.splitext(testname)[1]
        if ext == '.ptest':
            positions = True

        reader = csv.reader(open(testname), delimiter=';')

        test = []
        for row in reader:
            test.append(row)

        if init:
            fontname = 'amiri-regular.ttf'
            outname = testname+".test"
            outfd = open(outname, "w")
            outfd.write(initTest(test, fontname, positions))
            outfd.close()
            sys.exit(0)

        if positions:
            styles = ('regular', )
        else:
            styles = ('regular', 'bold', 'slanted', 'boldslanted')

        for style in styles:
            fontname = 'amiri-%s.ttf' % style
            passed, failed = runTest(test, fontname, positions)
            message = "%s: font '%s', %d passed, %d failed" %(os.path.basename(testname),
                    fontname, len(passed), len(failed))

            print message
            if failed:
                for test in failed:
                    print test
                    print "string:   \t", failed[test][0]
                    print "reference:\t", failed[test][1]
                    print "result:   \t", failed[test][2]
                sys.exit(1)
