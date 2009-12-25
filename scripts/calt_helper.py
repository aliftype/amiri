def addLookups(font, name):
	cname        = "'calt' "+name
	font.changed = True
	font.addLookup        (name,  "gsub_single", "ignore_marks", ())
	font.addLookup        (cname, "gsub_contextchain", "ignore_marks", (("calt",(("DFLT", ("dflt")),("arab",("dflt")))),))
	font.addLookupSubtable(name,  name+"-1" )
	font.addLookupSubtable(cname, cname+"-2")
	font.addLookupSubtable(cname, cname+"-1")

def addData(font, glyphs, name):
	for g in glyphs:
		bname = g.glyphname.split("_")[0]
		b = font.createChar(-1, bname)
		b.addPosSub(name+"-1", g.glyphname)

def buildCalt(data, font):
	name      = fontforge.askString("Rule name", "Type lookup name")
	selection = font.selection.byGlyphs
	if name:
		addLookups(font, name)
		addData(font, selection, name)
	else:
		fontforge.postError("No name specified", "You didn't specify a name. Doing nothing")

fontforge.registerMenuItem(buildCalt, None, None, "Font", "C", "Build Contextual Alternatives")
