import fontforge
import tempfile
import subprocess
import os

ttf = tempfile.NamedTemporaryFile(suffix=".ttf").name

viewer = "fontview"
flags  = ("opentype", "dummy-dsig", "round", "short-post")

def class2pair(font, remove):
    """Looks for any kerning classes in the font and converts it to
    RTL kerning pairs."""
    kern_pairs = 0
    kern_class = 0
    new_subtable = ""
    for lookup in font.gpos_lookups:
        if font.getLookupInfo(lookup)[0] == "gpos_pair":
            for subtable in font.getLookupSubtables(lookup):
                if font.isKerningClass(subtable):
                    kern_class += 1
                    new_subtable = subtable + " pairs"
                    font.addLookupSubtable(lookup, new_subtable)
                    kclass   = font.getKerningClass(subtable)
                    klasses1 = kclass[0]
                    klasses2 = kclass[1]
                    offsets  = kclass[2]

                    for klass1 in klasses1:
                        if klass1 != None:
                            for name in klass1:
                                glyph = font.createChar(-1, name)
                                for klass2 in klasses2:
                                    if klass2 != None:
                                        kern = offsets[klasses1.index(klass1)
                                                *len(klasses2)+
                                                klasses2.index(klass2)]
                                        if kern != 0:
                                            for glyph2 in klass2:
                                                glyph.addPosSub(new_subtable,
                                                        glyph2,
                                                        kern,0,kern,0,0,0,0,0)
					        font.changed = True
                                                kern_pairs  += 1
                    if remove:
                        font.removeLookupSubtable(subtable)
    return new_subtable

def Preview(re, obj):
    if type(obj).__name__ == "font":
        font = obj
    else:
        font = obj.font

    familyname = font.familyname
    changed = font.changed

    font.familyname = "%sPreview" %familyname
    new_sub = class2pair(font, False)
    font.generate(ttf,flags=flags)

    if new_sub:
        font.removeLookupSubtable(new_sub)
    font.familyname = familyname
    font.changed = changed

    if not re:
        cmd = "%s %s" %(viewer, ttf)
        subprocess.Popen(cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)


fontforge.registerMenuItem(
        Preview,None,None,("Font","Glyph"),"P","Preview","Preview font")
fontforge.registerMenuItem(
        Preview,None,True,("Font","Glyph"),"R","Preview","Re-view font")
