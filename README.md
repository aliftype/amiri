[![Build Status](https://travis-ci.com/alif-type/amiri.svg?branch=master)](https://travis-ci.com/alif-type/amiri)

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
modify. Amiri is available under the terms of [Open Font License][2], see the
included license file for more details.

Latest version of the Amiri font can be obtained from its web site:

> http://amirifont.org

Contributing
------------

To edit the font sources, you will need FontForge, preferably the latest
version. To install FontForge on Debian and Ubuntu:

    $ sudo apt-get install fontforge

You can then open the source files in FontForge and start editing, either from
GUI or from the command line:

    $ fontforge sources/Amiri-Regular.sfdir

To build the fonts you need a few Python packages:

    $ python -m venv amiri
    $ . amiri/bin/activate
    $ pip install -r requirements.txt

To build the font files run:

    $ make ttf

[1]: http://www.bibalex.org/bulaqpress/en/bulaq.htm "The Bulaq Press"
[2]: http://scripts.sil.org/OFL "The Open Font License"
