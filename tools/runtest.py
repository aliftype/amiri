#!/usr/bin/env python

import sys
import os
import csv

import harfbuzz as hb

HbFonts = {}
def getHbFont(fontname):
    if fontname not in HbFonts:
        with open(fontname, "rb") as fp:
            data = fp.read()
        blob = hb.Blob.create_for_array(data, hb.HARFBUZZ.MEMORY_MODE_READONLY)
        face = hb.Face.create(blob, 0, False)
        font = hb.Font.create(face)
        font.scale = (face.upem, face.upem)
        font.ot_set_funcs()

        HbFonts[fontname] = font

    return HbFonts[fontname]

def runHB(font, buf, direction, script, language, features, text, positions):
    buf.clear_contents()
    buf.add_str(text)
    buf.direction = hb.direction_from_string(direction)
    buf.script = hb.script_from_string(script)
    if language:
        buf.language = hb.Language.from_string(language)

    if features:
        features = [hb.Feature.from_string(fea) for fea in features.split(',')]
    else:
        features = []
    hb.shape(font, buf, features)

    info = buf.glyph_infos
    if positions:
        pos = buf.glyph_positions
        glyphs = []
        x = 0
        for i, p in zip(info, pos):
            glyph = font.get_glyph_name(i.codepoint)
            glyph += "@(%d,%d)" % (x + p.x_offset, p.y_offset)
            glyph += "+%d" % p.x_advance
            glyphs.append(glyph)
            x += p.x_advance
        out = "|".join(glyphs)
    else:
        out = "|".join([font.get_glyph_name(i.codepoint) for i in info])

    return "[%s]" % out

def runTest(test, fontname, positions):
    count = 0
    failed = {}
    passed = []
    font = getHbFont(fontname)
    buf = hb.Buffer.create()
    for row in test:
        count += 1
        direction, script, language, features, text, reference = row
        text = text.encode().decode('unicode-escape') if '\\' in text else text
        result = runHB(font, buf, direction, script, language, features, text, positions)
        if reference == result:
            passed.append(count)
        else:
            failed[count] = (direction, script, language, features, text, reference, result)

    return passed, failed

def initTest(test, fontname, positions):
    out = ""
    font = getHbFont(fontname)
    buf = hb.Buffer.create()
    for row in test:
        direction, script, language, features, enctext, reference = row
        text = enctext.encode().decode('unicode-escape') if '\\' in enctext else enctext
        result = runHB(font, buf, direction, script, language, features, text, positions)
        out += "%s;%s;%s\n" %(";".join(row[:4]), enctext, result)

    return out

if __name__ == '__main__':
    init = False
    positions = False
    args = sys.argv[1:]

    if len (sys.argv) > 2 and sys.argv[1] == "-i":
        init = True
        args = sys.argv[2:]

    if init is True:
        for testname in args:
            reader = csv.reader(open(testname), delimiter=';')
            test = []
            for row in reader:
                test.append(row)

            positions = os.path.splitext(testname)[1] == '.ptest'
            fontname = 'Amiri-Regular.ttf'
            outname = testname+".test"
            outfd = open(outname, "w")
            outfd.write(initTest(test, fontname, positions))
            outfd.close()
            sys.exit(0)

    styles = ('Regular', 'Bold', 'Slanted', 'BoldSlanted')
    for style in styles:
        fontname = 'Amiri-%s.ttf' % style
        print("   TEST\t%s" % fontname)
        for testname in args:
            positions = os.path.splitext(testname)[1] == '.ptest'

            if positions and style != "Regular":
                continue

            reader = csv.reader(open(testname), delimiter=';')

            test = []
            for row in reader:
                test.append(row)

            passed, failed = runTest(test, fontname, positions)
            if failed:
                message = "%s: font '%s', %d passed, %d failed" %(os.path.basename(testname),
                        fontname, len(passed), len(failed))

                print(message)
                for test in failed:
                    print(test)
                    print("direction:\t", failed[test][0])
                    print("script:   \t", failed[test][1])
                    print("language: \t", failed[test][2])
                    print("features: \t", failed[test][3])
                    print("string:   \t", failed[test][4])
                    print("reference:\t", failed[test][5])
                    print("result:   \t", failed[test][6])
                sys.exit(1)
