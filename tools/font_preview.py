import tempfile
import subprocess
import os

viewer    = "fv"
tempnames = {}

def Preview(re, font):
	otf = tempfile.NamedTemporaryFile(suffix=".otf", delete=False).name
	cmd = "%s %s" %(viewer, otf)
	if re and os.path.isfile(tempnames[font.fontname]):
		font.generate(tempnames[font.fontname])
	else:
		tempnames[font.fontname] = otf
		font.generate(otf)
		subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview, None, None, "Font", "P", "Preview", "Preview font")
fontforge.registerMenuItem(Preview, None, True, "Font", "R", "Preview", "Re-preview font")
