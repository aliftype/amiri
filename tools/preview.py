import fontforge
import tempfile
import subprocess
import os

viewer = "fontview"
flags  = ("opentype", "dummy-dsig", "round", "short-post")
out    = ""

def Preview(re, obj):
    if type(obj).__name__ == "font":
        font = obj
    else:
        font = obj.font

    global out

    if not out:
        if font.layers[1].is_quadratic:
            out = tempfile.NamedTemporaryFile(suffix=".ttf").name
        else:
            out = tempfile.NamedTemporaryFile(suffix=".otf").name

    font.generate(out, flags=flags)

    if not re:
        cmd = "%s %s" %(viewer, out)
        subprocess.Popen(cmd,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview, None, None, ("Font", "Glyph"), "P", "Preview", "Preview font")
fontforge.registerMenuItem(Preview, None, True, ("Font", "Glyph"), "R", "Preview", "Re-view font")
