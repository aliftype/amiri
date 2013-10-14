#!/usr/bin/env python
import sys
import os
import getopt
import random
import subprocess
import re

def random_color(match):
    color = random.randint(0, 0xFFFFFF)
    return "<span color='#%06X'>%s</span>" %(color, match.group())

def colorize(string):
    return "<span fallback='no'>%s</span>" %re.sub(r"\S", random_color, string).strip()

def main():
    try:
        opts, args = getopt.gnu_getopt(
                # all the options recognised by pango-view
                sys.argv[1:], "qho:n:w:t:",
                ["no-auto-dir", "backend=", "background=", "no-display",
                    "dpi=", "align=", "ellipsize=", "font=", "foreground=",
                    "gravity=", "gravity-hint=", "header", "height=", "rtl",
                    "hinting=", "indent=", "justify", "language=", "margin=",
                    "markup", "output=", "pangorc=", "pixels", "rotate=",
                    "runs=", "single-par", "text=", "version", "waterfall",
                    "width=", "wrap=", "annotate=","help", "help-all",
                    "help-cairo"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:
        if o in ("-t", "--text"):
            i = opts.index((o, a))
            opts.remove((o, a))
            opts.insert(i, (o, colorize(a.decode("utf-8"))))

    cmd = ["pango-view", "--markup"]

    for opt in opts:
        if opt[1]:
            cmd.extend(opt)
        else:
            cmd.append(opt[0])

    if args:
        if os.path.isfile(args[-1]):
            file = open(args[-1], "r")
            text = colorize(file.read().decode("utf-8"))
            cmd.extend(["-t", text])
        else:
            print "Failed to open file '%s':" % args[-1],
            print "No such file or directory"

    subprocess.call(cmd)

if __name__=="__main__":
    main()
