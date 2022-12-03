import sys
from fontTools.ttLib import TTFont

for path in sys.argv[1:]:
    font = TTFont(path)
    font["post"].formatType = 3
    font.save(path)
