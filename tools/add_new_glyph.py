# encoding: utf8
def addCharacters(crap, font):
    text = fontforge.askString("Add charcter", u"model new mark₁ mark₂ ...")
    text = text.split()
    if len(text) < 3:
        fontforge.postError("Error", "Not enough entries")
    else:
        addCharacter(font, text[0], text[1], text[2:])

def addCharacter(font, model, new, marks):
    names = []
    for glyph in font.glyphs():
        if (glyph.glyphname == model) or (model+"." in glyph.glyphname):
            for ref in glyph.references:
                if (font[ref[0]].glyphclass == "baseglyph") or (font[ref[0]].glyphclass == "automatic"):
                    names.append((glyph.glyphname, ref[0], glyph.anchorPoints))

    for name, base, anchors in names:
        if "." in name:
            glyph = font.createChar(-1, name.replace(model+'.', new+'.'))
        else:
            glyph = font.createChar(-1, new)

        glyph.addReference(base)
        glyph.useRefsMetrics(base)
        for mark in marks:
            glyph.addReference(mark)
        glyph.anchorPoints = anchors

fontforge.registerMenuItem(addCharacters, None, None, "Font", None, "Add Characters")
