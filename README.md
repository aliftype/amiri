[![Build](https://github.com/aliftype/amiri/actions/workflows/build.yml/badge.svg)](https://github.com/aliftype/amiri/actions/workflows/build.yml)

Amiri
=====

Amiri (أميري) is a classical Arabic typeface in Naskh style for typesetting books and
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

> https://aliftype.com/amiri

Development status
------------------

Amiri was actively developed between 2008–2022, when version 1 was released and
it was then considered mature enough that not further development is planned.
No typeface is ever complete, but maintaining Amiri is increasingly time and
effort-consuming due to a combination of decisions taken early on due to
software limitations at the time its development started, as well as extensive
character and glyph coverage. Amiri development might be restarted in the
future under a different name with less backward-compatibility constraints, but
nothing concrete is currently planed.

Building
--------

To build the fonts you need a few Python packages:

    $ python -m venv amiri
    $ . amiri/bin/activate
    $ pip install -r requirements.txt

To build the font files run:

    $ make ttf

[1]: https://www.bibalex.org/bulaqpress/en/bulaq.htm "The Bulaq Press"
[2]: https://openfontlicense.org "The Open Font License"
