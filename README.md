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

Latest version of the Amiri font can be optained from its web site:

> http://amirifont.org

Contribution
============
Amiri is a free and open source project that everyone is encouraged to use and
modify. Amiri is avialable under the terms of [Open Font License][2], see the
included license file for more details.

Editing the Font Files
--------------
Before you can edit the font files, you need to prepare the environment:


    $ sudo apt-get install fontforge python-fontforge gpp
    $ mkvirtualenv amiri --system-site-packages
    $ pip install fonttools brotli

The commands above assumes a Linux Debian OS, but should be portable to other
Linux distros and possibly Mac OS.

Edit the font files with `$ fontforge sources/Amiri-Regular.sfdir/`,
save the changes.

To create the font files run `$ make all`


[1]: http://www.bibalex.org/bulaqpress/en/bulaq.htm "The Bulaq Press"
[2]: http://scripts.sil.org/OFL "The Open Font License"
