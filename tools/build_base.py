def buildAccented(data, glyph):
	if len(glyph.getPosSub("'ccmp' Glyph Decomposition-1")) == 1:
		ccmp = glyph.getPosSub("'ccmp' Glyph Decomposition-1")[0]
		glyph.clear()
		glyph.addReference(ccmp[2])
		glyph.useRefsMetrics(ccmp[2])

		if len(ccmp) > 3:
			glyph.appendAccent(name=ccmp[3])

		return 1

def drawBbox(data, glyph):
	if data:
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

	if data == 1:
		glyph.right_side_bearing = 0
		glyph.left_side_bearing  = 0

def buildBase(data, font):
	selection = font.selection.byGlyphs
	for g in selection:
		drawBbox(buildAccented(data, g), g)

fontforge.registerMenuItem(buildBase,     None, None, "Font",  None, "Bulaq", "Base", "Build base glyphs")
fontforge.registerMenuItem(buildAccented, None, None, "Glyph", None, "Bulaq", "Base", "Build glyph from 'ccmp'")
fontforge.registerMenuItem(drawBbox,      None,    2, "Glyph", None, "Bulaq", "Base", "Draw bounding box'")
