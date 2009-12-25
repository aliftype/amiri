import tempfile
import subprocess
import os

viewer = "fv"

def Preview(re, font):
	otf = "%s/%s.otf" %(tempfile.gettempdir(), font.fontname)
	cmd = "%s %s" %(viewer, otf)
	if re and os.path.isfile(otf):
		font.generate(otf)
	else:
		font.generate(otf)
		subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview, None, None, "Font", None, "Preview font")
fontforge.registerMenuItem(Preview, None, True, "Font", None, "Re-preview font")
