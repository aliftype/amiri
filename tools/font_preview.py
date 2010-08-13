import subprocess
import os

viewer    = "fv"
sep       = os.path.sep

def Preview(re, font):
	ttf = "..%s%s.%s" %(sep, font.default_base_filename, "ttf")
	font.generate(ttf)
	if not re:
	        cmd = "%s %s" %(viewer, ttf)
		subprocess.Popen(cmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview,
        None, None, "Font", "P", "Preview", "Preview font")
fontforge.registerMenuItem(Preview,
        None, True, "Font", "R", "Preview", "Re-preview font")
