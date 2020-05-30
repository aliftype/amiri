"""
Script to do changes required for Google Fonts that we can’t have by default.
Currently just renames Slanted to Italic.
"""

from fontTools.ttLib import TTFont

for path in ("Amiri-Slanted.ttf", "Amiri-BoldSlanted.ttf"):
  with TTFont(path) as font:
    for name in font["name"].names:
      if name.nameID in (2, 3, 4, 6):
        name.string = str(name).replace("Slanted", "Italic")
    font.save(path.replace("Slanted", "Italic"))
