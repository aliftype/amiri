[![Build Status](https://travis-ci.org/alif-type/amiri.svg?branch=master)](https://travis-ci.org/alif-type/amiri)

Amiri Font
==========

Amiri is a classical Arabic typeface in Naskh style for typesetting books and
other running text.

Amiri is a revival of the beautiful typeface pioneered in early 20th century by
[Bulaq Press][1] in Cairo, also known as Amiria Press, after which the font is
named.

The uniqueness of this typeface comes from its superb balance between the
beauty of Naskh calligraphy on one hand, the constraints and requirements of
elegant typography on the other. Also, it is one of the few metal typefaces
that were used in typesetting the Koran, making it a good source for a digital
typeface to be used in typesetting Koranic verses.

Amiri project aims at the revival of the aesthetics and traditions of Arabic
typesetting, and adapting it to the era of digital typesetting, in a publicly
available form.

Amiri is a free and open source project that everyone is encouraged to use and
modify. Amiri is avialable under the terms of [Open Font License][2], see the
included license file for more details.

Latest version of the Amiri font can be optained from its web site:

> http://amirifont.org

Contributing
------------

To edit the font sources, you will need FontForge, preferably the latest
version. To install FontForge on Debian and Ubuntu:

    $ sudo apt-get install fontforge

You can then open the source files in FontForge and start editing, either from
GUI or from the command line:

    $ fontforge sources/Amiri-Regular.sfdir

To build the fonts you need FontForge Python module, gpp and FontTools:

    $ sudo apt-get install python-fontforge gpp
    $ python -m venv amiri --system-site-packages
    $ . amiri/bin/activate
    $ pip install fonttools brotli

To build the font files run:

    $ make ttf

To build the font files along with the web files; run:

    $ make web

Ubuntu 16.04 Contributors
-------------------------

You might face an error with importing fontforge

    File "tools/build.py", line 18, in <module>
        import fontforge
    ImportError: No module named fontforge

This is because fontforge does not work properly with Python 3 on Ubuntu 16.04.
To build the fonts with Python version 2.7 ; install FontForge Python
module by following the instructions from the [official documentation][3]. But
make sure to enable python extension and scripting for Python 2. Use the following
commands instead of the original in the last step of the installation:

    $ cd fontforge
    $ ./bootstrap
    $ ./configure --enable-python-extension --enable-python-scripting=2
    $ make
    $ sudo make install
    $ sudo ldconfig 

After that, return back to the directory of the amiri repository and continue
with python-fontforge, gpp, and the virtual environment
 
    $ sudo apt-get install python-fontforge gpp
    $ virtualenv amiri --system-site-packages
    $ . amiri/bin/activate
    $ pip install fonttools brotli

[1]: http://www.bibalex.org/bulaqpress/en/bulaq.htm "The Bulaq Press"
[2]: http://scripts.sil.org/OFL "The Open Font License"
[3]: https://github.com/fontforge/fontforge/blob/master/INSTALL-git.md "FontForge official documentation"