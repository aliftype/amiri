def addLookups(font, name):
	cname        = "'calt' "+name
	font.changed = True
	font.addLookup        (name,  "gsub_single", "ignore_marks", ())
	font.addLookup        (cname, "gsub_contextchain", "ignore_marks", (("calt",(("DFLT", ("dflt")),("arab",("dflt")))),))
	font.addLookupSubtable(name,  name+"-1" )
	font.addLookupSubtable(cname, cname+"-2")
	font.addLookupSubtable(cname, cname+"-1")
	fontforge.postNotice("Lookups created", "Created `%s' and `%s' lookups" %(name, cname))

def addData(font, glyphs, name):
	for g in glyphs:
		bname = g.glyphname.split("_")[0]
		b = font.createChar(-1, bname)
		b.addPosSub(name+"-1", g.glyphname)

def buildCalt(data, font):
	selection = font.selection.byGlyphs
	for g in selection:
		name = g.glyphname.split("_")[-1]
		break
	addLookups(font, name)
	addData(font, selection, name)

fontforge.registerMenuItem(buildCalt, None, None, "Font", "C", "Bulaq", "Build Contextual Alternatives")
