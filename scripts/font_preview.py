import tempfile
import commands

viewer = "fv"

def Preview(data, font):
	otf = tempfile.NamedTemporaryFile(suffix=".otf", delete=False).name
	cmd = "%s %s" %(viewer, otf)
	font.generate(otf)
	(exitstatus, outtext) = commands.getstatusoutput(cmd)


fontforge.registerMenuItem(Preview, None, None, "Font", None, "Preview font")
