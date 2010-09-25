#!/usr/bin/python

import fontforge
import sys

def drawSide(glyph, block=False):
    if glyph.width != 0:
        glyph.correctDirection()
        glyph.removeOverlap()
        bbox = glyph.boundingBox()

        ymax = bbox[3]
        ymin = bbox[1]

        xmax = glyph.width
        xmin = 0

        pen  = glyph.glyphPen(replace=False)

        pen.moveTo(xmin, ymin)
        pen.lineTo(xmax, ymin)
        pen.lineTo(xmax, ymax)
        pen.lineTo(xmin, ymax)
        pen.lineTo(xmin, ymin)
        pen.closePath()

        if ymin < -20:
            pen.moveTo(20, 0)
            pen.lineTo(xmax-20, 0)
            pen.lineTo(xmax-20, ymin+20)
            pen.lineTo(20, ymin+20)
            pen.lineTo(20, 0)
            pen.closePath()

            pen.moveTo(20, 20)
            pen.lineTo(20, ymax-20)
            pen.lineTo(xmax-20, ymax-20)
            pen.lineTo(xmax-20, 20)
            pen.lineTo(20, 20)
            pen.closePath()
        else:
            if ymin > 20:
                pen.moveTo(0, 0)
                pen.lineTo(xmax, 0)
                pen.lineTo(xmax, 20)
                pen.lineTo(0, 20)
                pen.lineTo(0, 0)
                pen.closePath()

            pen.moveTo(xmin+20, ymin+20)
            pen.lineTo(xmin+20, ymax-20)
            pen.lineTo(xmax-20, ymax-20)
            pen.lineTo(xmax-20, ymin+20)
            pen.lineTo(xmin+20, ymin+20)
            pen.closePath()

        pen = None
    else:
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

        pen.moveTo(xmin+20, ymin+20)
        pen.lineTo(xmin+20, ymax-20)
        pen.lineTo(xmax-20, ymax-20)
        pen.lineTo(xmax-20, ymin+20)
        pen.lineTo(xmin+20, ymin+20)
        pen.closePath()

	pen = None

font = fontforge.open(sys.argv[1])
for glyph in font.glyphs():
    drawSide(glyph, False)
font.save()
