import fontforge
import tempfile
import subprocess
import os

ttf = tempfile.NamedTemporaryFile(suffix=".ttf").name

viewer = "fontview"
flags  = ("opentype", "dummy-dsig", "round", "short-post")

def Preview(re, obj):
    if type(obj).__name__ == "font":
        font = obj
    else:
        font = obj.font

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
