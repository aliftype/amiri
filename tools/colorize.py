#!/usr/bin/python
import sys
import random
import subprocess

colors = [
    "aquamarine", "aquamarine2", "aquamarine3", "aquamarine4", "bisque",
    "bisque2", "bisque3", "bisque4", "black", "BlanchedAlmond", "blue",
    "blue2", "blue3", "blue4", "BlueViolet", "brown", "brown2",
    "brown3", "brown4", "burlywood", "burlywood2", "burlywood3",
    "burlywood4", "CadetBlue", "CadetBlue2", "CadetBlue3", "CadetBlue4",
    "chartreuse", "chartreuse2", "chartreuse3", "chartreuse4",
    "coral", "coral2", "coral3", "coral4", "CornflowerBlue", "cyan",
    "cyan2", "cyan3", "cyan4", "DarkBlue", "DarkCyan", "DarkGoldenrod",
    "DarkGoldenrod2", "DarkGoldenrod3", "DarkGoldenrod4", "DarkGreen",
    "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOliveGreen2",
    "DarkOliveGreen3", "DarkOliveGreen4", "DarkOrange", "DarkOrange2",
    "DarkOrange3", "DarkOrange4", "DarkOrchid", "DarkOrchid2",
    "DarkOrchid3", "DarkOrchid4", "DarkRed", "DarkSalmon", "DarkSeaGreen",
    "DarkSeaGreen2", "DarkSeaGreen3", "DarkSeaGreen4", "DarkSlateBlue",
    "DarkTurquoise", "DarkViolet",   "DeepPink", "DeepPink2",
    "DeepPink3", "DeepPink4", "DeepSkyBlue", "DeepSkyBlue2",
    "DeepSkyBlue3", "DeepSkyBlue4", "DodgerBlue", "DodgerBlue2",
    "DodgerBlue3", "DodgerBlue4", "firebrick", "firebrick2", "firebrick3",
    "firebrick4", "ForestGreen", "gainsboro", "gold", "gold2", "gold3",
    "gold4", "goldenrod", "goldenrod2", "goldenrod3", "goldenrod4",
    "green", "green2", "green3", "green4", "GreenYellow", "HotPink2",
    "HotPink3", "HotPink4", "IndianRed", "IndianRed2", "IndianRed3",
    "IndianRed4", "khaki", "khaki2", "khaki3", "khaki4", "LawnGreen",
    "LemonChiffon", "LemonChiffon2", "LemonChiffon3", "LemonChiffon4",
    "LimeGreen", "magenta", "magenta2", "magenta3", "magenta4", "maroon",
    "maroon2", "maroon3", "maroon4", "MediumAquamarine", "MediumBlue",
    "MediumOrchid", "MediumOrchid2", "MediumOrchid3", "MediumOrchid4",
    "MediumPurple", "MediumPurple2", "MediumPurple3", "MediumPurple4",
    "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen",
    "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MistyRose",
    "MistyRose2", "MistyRose3", "MistyRose4", "navy", "NavyBlue",
    "OliveDrab", "OliveDrab2", "OliveDrab3", "OliveDrab4", "orange",
    "orange2", "orange3", "orange4", "OrangeRed", "OrangeRed2",
    "OrangeRed3", "OrangeRed4", "orchid", "orchid2", "orchid3",
    "orchid4", "PaleGoldenrod", "PaleGreen", "PaleGreen2", "PaleGreen3",
    "PaleGreen4", "PaleTurquoise", "PaleTurquoise2", "PaleTurquoise3",
    "PaleTurquoise4", "PaleVioletRed", "PaleVioletRed2", "PaleVioletRed3",
    "PaleVioletRed4", "PeachPuff", "PeachPuff2", "PeachPuff3",
    "PeachPuff4", "peru", "pink", "pink2", "pink3", "pink4", "plum",
    "plum2", "plum3", "plum4", "PowderBlue", "purple", "purple2",
    "purple3", "purple4", "red", "red2", "red3", "red4", "RosyBrown",
    "RosyBrown2", "RosyBrown3", "RosyBrown4", "RoyalBlue", "RoyalBlue2",
    "RoyalBlue3", "RoyalBlue4", "SaddleBrown", "salmon", "salmon2",
    "salmon3", "salmon4", "SandyBrown", "SeaGreen", "SeaGreen2",
    "SeaGreen3", "SeaGreen4", "sienna", "sienna2", "sienna3", "sienna4",
    "SkyBlue", "SkyBlue2", "SkyBlue3", "SkyBlue4", "SlateBlue",
    "SlateBlue2", "SlateBlue3", "SlateBlue4", "SpringGreen",
    "SpringGreen2", "SpringGreen3", "SpringGreen4", "SteelBlue",
    "SteelBlue2", "SteelBlue3", "SteelBlue4", "tan", "tan2", "tan3",
    "tan4", "thistle", "thistle2", "thistle3", "thistle4", "tomato",
    "tomato2", "tomato3", "tomato4", "turquoise", "turquoise2",
    "turquoise3", "turquoise4", "violet", "VioletRed", "VioletRed2",
    "VioletRed3", "VioletRed4", "wheat", "wheat2", "wheat3", "wheat4",
    "yellow", "yellow2",
]

text = ""
pcol = ""

for i in sys.argv[1].decode("utf8"):
    if i == " ":
        text += i
    else:
        color = random.choice(colors)
        text += "<span color='%s'>%s</span>" %(color, i)
        pcol += " "+color

subprocess.call(
        [
            "pango-view",
            "--markup",
            "--font=Amiri 70",
            "-t",
            text,
        ]
    )
