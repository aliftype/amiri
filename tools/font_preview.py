import subprocess
import os

viewer = "fv"
flags  = ("opentype", "dummy-dsig", "round", "short-post")

def Preview(re, obj):
    # XXX: stupid hack
    if str(type(obj)) == "<type 'fontforge.font'>":
        font = obj
    else:
        font = obj.font

    ttf = "..%s%s.%s" %(os.path.sep, font.default_base_filename, "ttf")
    font.generate(ttf,flags=flags)
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
