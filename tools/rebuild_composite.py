top_marks = ("Dot.a", "TwoDots.a", "ThreeDots.a", "iThreeDots.a",
             "vTwoDots.a", "FourDots.a", "hThreeDots.a", "aTwo.above",
             "aThree.above", "smalltaa.above", "uni0654", "uni0674",
             "hamza.above", "smallv.above", "smallv.above.inverted")
bot_marks = ("Dot.b", "TwoDots.b", "ThreeDots.b", "iThreeDots.b", "vTwoDots.b",
             "FourDots.b", "hThreeDots.b", "ring.below", "aFour.below",
             "smallv.below", "smallv.below.inverted", "smallv.below.low",
             "smallv.below.inverted.low",
             "Dot.b.l", "TwoDots.b.l", "ThreeDots.b.l", "iThreeDots.b.l", "vTwoDots.b.l",
             "FourDots.b.l", "hThreeDots.b.l")

def RebuildGlyph(glyph):
    font = glyph.font
    base = ""
    marks = []
    anchors = []
    for ref in glyph.references:
        klass = font[ref[0]].glyphclass
        if klass != "mark" and (klass == "baseglyph" or klass == "automatic"):
            if not base:
                base = ref[0]
            else:
                print "error"
        elif klass == "mark":
            marks.append(ref[0])

    for a in glyph.anchorPoints:
        anchors.append(a[0])

    glyph.clear()
    glyph.addReference(base)
    glyph.useRefsMetrics(base)
    for mark in marks:
        glyph.appendAccent(mark)
        glyph.build()
    for anchor in font[base].anchorPoints:
        if anchor[0] in anchors:
            glyph.addAnchorPoint(anchor[0], anchor[1], anchor[2], anchor[3])

def FixTashilOverTopMarks(glyph):
    font = glyph.font

    for ref in glyph.references:
        if ref[0] in top_marks:
            for anchor in glyph.anchorPoints:
                if anchor[0] == "TashkilAbove":
                    oldanchor = anchor

            transform = ref[1]
            ymax = font[ref[0]].boundingBox()[3]

            if oldanchor[-1] < (ymax + transform[-1]):
                for anchor in font[ref[0]].anchorPoints:
                    if anchor[0] == "TashkilAboveDot" or anchor[0] =="TashkilTashkilAbove":
                        newanchor = anchor
                glyph.addAnchorPoint("TashkilAbove", "base", newanchor[-2] + transform[-2], newanchor[-1] + transform[-1] - 100)

def FixTashilUnderBottomMarks(glyph):
    font = glyph.font
    for ref in glyph.references:
        if ref[0] in bot_marks:
            for anchor in glyph.anchorPoints:
                if anchor[0] == "TashkilBelow":
                    oldanchor = anchor

            transform = ref[1]
            ymin = font[ref[0]].boundingBox()[1]

            if oldanchor[-1] > (ymin + transform[-1]):
                for anchor in font[ref[0]].anchorPoints:
                    if anchor[0] == "TashkilBelowDot":
                        newanchor = anchor
                glyph.addAnchorPoint("TashkilBelow", "base", newanchor[-2] + transform[-2], newanchor[-1] + transform[-1])

def RebuildGlyphs(crap, font):
    for glyph in font.selection.byGlyphs:
        RebuildGlyph(glyph)
        FixTashilUnderBottomMarks(glyph)
        FixTashilOverTopMarks(glyph)

fontforge.registerMenuItem(RebuildGlyphs, None, None, "Font", None, "Rebuild Glyphs")
