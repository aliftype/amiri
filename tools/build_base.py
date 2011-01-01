def buildAccented(box, glyph):
    if len(glyph.getPosSub("'isol' Isolated Forms-1")) == 1:
        ccmp = glyph.getPosSub("'isol' Isolated Forms-1")[0]
        glyph.clear()
        glyph.addReference(ccmp[2])
        glyph.useRefsMetrics(ccmp[2])

        if len(ccmp) > 3:
            for accent in ccmp[3:]:
                glyph.appendAccent(accent)

        if box:
            drawBbox(glyph)

def drawBbox(glyph):
    bbox = glyph.boundingBox()
    xmin = bbox[0]
    ymin = bbox[1]
    xmax = bbox[2]
    ymax = bbox[3]

    pen  = glyph.glyphPen(replace=False)

    pen.moveTo(xmin, ymin)
    pen.lineTo(xmax, ymin)
    pen.lineTo(xmax, ymax)
    pen.lineTo(xmin, ymax)
    pen.lineTo(xmin, ymin)
    pen.closePath()

    pen = None

def buildBase(box, font):
    selection = font.selection.byGlyphs
    for g in selection:
        buildAccented(box, g)

fontforge.registerMenuItem(buildBase,     None, None, "Font",  None, "Amiri", "Build base glyphs")
fontforge.registerMenuItem(buildBase,     None, True, "Font",  None, "Amiri", "Build base glyphs (boxed)")
fontforge.registerMenuItem(buildAccented, None, None, "Glyph", None, "Amiri", "Build base glyph")
fontforge.registerMenuItem(buildAccented, None, True, "Glyph", None, "Amiri", "Build base glyph (boxed)")
