import tempfile
import subprocess

viewer = "fv"

def Preview(data, font):
	otf = tempfile.NamedTemporaryFile(suffix=".otf", delete=False).name
	cmd = "%s %s" %(viewer, otf)
	font.generate(otf)
	subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


fontforge.registerMenuItem(Preview, None, None, "Font", None, "Preview font")
