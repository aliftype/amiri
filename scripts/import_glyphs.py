import fontforge
import glob
import os

font = fontforge.open("AmiriText-Regular.sfd")
svgs = glob.glob("glyphs/*.svg")
svgs.sort()

for svg in svgs:
    name  = os.path.basename(svg).replace(".svg", "")
    print "Importing: %s" % name
    glyph = font.createChar(-1, name)
    glyph.clear()
    glyph.importOutlines(svg)
#   glyph.round()

font.save()
