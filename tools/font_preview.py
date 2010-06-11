import tempfile
import subprocess
import os

viewer    = "fv"
tempnames = {}

def Preview(re, font):
	ttf = tempfile.NamedTemporaryFile(suffix=".ttf", delete=False).name
	cmd = "%s %s" %(viewer, ttf)
	if re and os.path.isfile(tempnames[font.fontname]):
		font.generate(tempnames[font.fontname])
	else:
		tempnames[font.fontname] = ttf
		font.generate(ttf)
		subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview, None, None, "Font", "P", "Preview", "Preview font")
fontforge.registerMenuItem(Preview, None, True, "Font", "R", "Preview", "Re-preview font")
