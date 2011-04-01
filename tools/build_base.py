def buildBase(box, glyph):
    if len(glyph.getPosSub("'isol' Isolated Forms in Arabic lookup 0 subtable")) == 1:
        ccmp = glyph.getPosSub("'isol' Isolated Forms in Arabic lookup 0 subtable")[0]
        glyph.clear()
        glyph.addReference(ccmp[2])
        glyph.useRefsMetrics(ccmp[2])

        if len(ccmp) > 3:
            for accent in ccmp[3:]:
                glyph.appendAccent(accent)

        if box:
            drawBbox(None,glyph)

def drawBbox(dummy, glyph):
    xmin, ymin, xmax, ymax = glyph.boundingBox()

    pen  = glyph.glyphPen(replace=False)

    pen.moveTo(xmin, ymin)
    pen.lineTo(xmax, ymin)
    pen.lineTo(xmax, ymax)
    pen.lineTo(xmin, ymax)
    pen.lineTo(xmin, ymin)
    pen.closePath()

    pen = None

def buildBases(box, font):
    selection = font.selection.byGlyphs
    for g in selection:
        buildBase(box, g)

def drawBboxes(dummy, font):
    selection = font.selection.byGlyphs
    for g in selection:
        drawBbox(dummy, g)

fontforge.registerMenuItem(drawBbox,   None, None, "Glyph", None, "Amiri", "Draw bounding box")
fontforge.registerMenuItem(buildBase,  None, None, "Glyph", None, "Amiri", "Build base glyph")
fontforge.registerMenuItem(buildBase,  None, True, "Glyph", None, "Amiri", "Build base glyph (boxed)")
fontforge.registerMenuItem(drawBboxes, None, None, "Font",  None, "Amiri", "Draw bounding box")
fontforge.registerMenuItem(buildBases, None, None, "Font",  None, "Amiri", "Build base glyphs")
fontforge.registerMenuItem(buildBases, None, True, "Font",  None, "Amiri", "Build base glyphs (boxed)")
