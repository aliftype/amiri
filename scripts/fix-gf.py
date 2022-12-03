"""
Script to do changes required for Google Fonts that we can’t have by default.
"""

from fontTools.ttLib import TTFont
import shutil
import os


GF_DIR = "gf_fonts"

if os.path.exists(GF_DIR):
  shutil.rmtree(GF_DIR)
os.mkdir(GF_DIR)


for path in ("Amiri-Italic.ttf", "Amiri-BoldItalic.ttf", "Amiri-Regular.ttf", "Amiri-Bold.ttf"):
  shutil.copy(path, GF_DIR)


colr_font = TTFont("AmiriQuranColored.ttf")
name_tbl = colr_font["name"]
for name_record in colr_font["name"].names:
  name_tbl.setName(
    name_record.toUnicode().replace("Colored", "").strip().replace("  ", " "),
    name_record.nameID,
    name_record.platformID,
    name_record.platEncID,
    name_record.langID,
  )
colr_font.save(os.path.join(GF_DIR, "AmiriQuran-Regular.ttf"))