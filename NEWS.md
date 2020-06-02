Amiri 0.113 (2020-06-02)
------------------------

* Add U+08BA, U+08B6, U+08B7, U+08B8, and U+08B9.
* Bug fixes:
  - https://github.com/alif-type/amiri/issues/172
  - https://github.com/alif-type/amiri/issues/187
* Add ligature carets to Latin ligatures.
* Building the fonts no longer requires FontForge.

Amiri 0.112 (2019-09-29)
------------------------

* Fix dot below (U+065C) and make it rounded not rectangular.
* Add an Amiri.fontspec file for use with LaTeX fontspec package (#139).
* Make the build reproducible.
* Fix some misplaced Latin accents.
* Add alternate comma and semicolon for Sindhi and Malay, and can be enabled
  with “ss08” feature as well (#145).
* Fix Rohingya tones positioning a bit (#155).
* Don’t make rounded guillemots the default as they are meant to be only for
  Arabic.
* Make narrow no break space as wide as thin space (#177).
* Fix handling of several Quranic small letters to follow latest Unicode
  recommendations.

Amiri 0.111 (2017-12-30)
------------------------

* Drop TTF files from the web fonts archive, WOFF and WOFF2 should be all one
  needs now.
* Cosmetic changes to the CSS snippet.
* Fix kerning of the new Kaf glyphs introduced in the previous release.
* Add a font table document for the Quran font since it has different character
  coverage.
* Removed the `ccmp` feature composing decomposed Latin base/accent
  combinations supported by the font. HarfBuzz does this in a bit smarter way,
  users of other engines can apply Unicode normalization to the input text if
  this is needed.
* Fix wrong glyph class for U+0674 ARABIC LETTER HIGH HAMZA, causing it to be
  incorrectly treated as a zero width mark:
  https://github.com/alif-type/amiri/issues/138.
* Drop localized Arabic names from the font (like style names), their support
  in application is spotty, also it is a bit Ugly to have the font presented
  with mixed language name, e.g. “Amiri عادي”, in some applications under
  Arabic locales.
* Allow Kashida around floating Hamza:
  https://github.com/alif-type/amiri/issues/137
* Colorize Hamza above mark in colored Quran font:
  https://github.com/alif-type/amiri/issues/136
* Change the shape of Damma used in U+06C7 & U+0677:
  https://github.com/alif-type/amiri/issues/123
* Other smaller fixes.
* OpenType layout tables are now compiled with FontTool’s feaLib instead of my
  FontForge fork. This is an attempt to make building the fonts from source
  simpler for others and more predictable.
* The font can now be built with Python 3, by calling `make PY2=python3`.
* The font can be also built with upstream FontForge now, though the result
  might be slightly different from the pre-built fonts.

Amiri 0.110 (2017-12-20)
------------------------
* New Glyphs
    - U+0604 ARABIC SIGN SAMVAT.
    - Alternate glyph for U+1EE13 ARABIC MATHEMATICAL REH.
    - Localized Kashmiri digits.
    - Alternate Kaf when followed by medial Heh

* Fixes:
    - Fix rendering of Amiri Quran Colored on Windows.
    - Improve Hamza below positioning in Amiri Quran.
    - Make U+0608 ARABIC RAY look like نق not just ق.
    - Make U+00B7 MIDDLE DOT the same width as space.
    - Keep exclamation mark upright in slanted fonts.
    - Make the الله combination work in better in some faulty applications.
    - Allow فالله/بالله/تالله/والله to take the special form.
    - Improve U+0674 ARABIC LETTER HIGH HAMZA by making it bigger and not
      zero-width, since it is a variant of Hamza and not a combining mark.
    - Improve the design of U+0600 ARABIC NUMBER SIGN to derive from the Urdu
      word نمرة.
    - Improve small Noon placement over Kashida.
    - Allow marks over small Yeh and Noon.
    - Greatly improve the handling of curvilinear Kashida.
    - Disable “لبمـ” and “ببحـ” combinations in Quran font.

* New features:
    - Add `ss07` to disable curvilinear Kashida.
    - Small improvements to the documentation.

Amiri 0.109 (2016-11-20)
------------------------
* New glyphs:
    - A new stylistic set (`ss06`) to avoid automatically adding ◌ّٰ above لله.
    - A localised &.
    - U+1EEF0 ARABIC MATHEMATICAL OPERATOR MEEM WITH HAH WITH TATWEEL (𞻰).
    - U+1EEF1 ARABIC MATHEMATICAL OPERATOR HAH WITH DAL (𞻱).
    - Adding missing forms of U+06C2.

* Fixes:
    - Fix clipping of some vowel marks in Microsoft Office.
    - Add descriptive stylistic sets names to the font.
    - Many improvements to Amiri Quran Colored, including revamped color
      palette by Munzir Taha.
    - Improve and redo most of the Arabic math alphanumeric symbols.
    - https://github.com/khaledhosny/quran-data/issues/1
    - https://github.com/khaledhosny/quran-data/issues/4
    - https://github.com/alif-type/amiri-font/issues/90
    - https://github.com/alif-type/amiri-font/issues/106

Amiri 0.108 (2015-09-21)
------------------------
* New glyphs:
    - New design of ه in ـهي combination.
    - Alternate numbers for use in fractions, accessible with the OpenType
      features `numr` and `dnom`.
    - The new Arabic Extended-A vowel marks, in the range U+08E4–08FE.
    - Redesign the U+06C1 forms to make it distinctive from U+06BE.
    - Add “جل جلاله” symbol, U+FDFB.

* Fixes:
    - No longer replace two successive *fatha*, *damma* or *kasra* with a
      sequential *tanween* form, the characters U+08F0, U+08F1 and U+08F2
      should be used instead.
    - Many kerning improvements.
    - Workaround a bug in Core Text (Mac OS X text layout engine) that break
      the لله ligature.
    - All forms of U+06BA are now dotless, per Unicode standard.
    - Initial and medial forms of U+063E, U+063F, U+077A and U+077B were
      missing.
    - The dots in initial and medial forms of U+06BD should be inverted.

* New fonts:
    - A coloured version of the Amiri Quran font that gives the vowels and
      Quranic annotation marks distinctive colours. This font uses the new
      `COLR`/`CPAL` font tables which are currently supported only by Firefox
      (all platforms) and MS Internet Explorer/Edge (Windows 8.1 and above).
    - The webfonts now include WOFF 2.0 files as well.

Amiri 0.107 (2013-12-30)
------------------------
* New glyphs:
    - Arabic math letters from Arabic Mathematical Alphabetic Symbols block
      (U+1EE00–U+1EEFF).
    - Optional support for placing the kasra below the shadda, with `ss05`
      feature.
    - Missing proportional LTR digits in the slanted font.

* Fixes:
    - Reverted the lowering of marks above wide isolated glyphs, it made the marks
      look weird relative to other ones.
    - Fixed the position of marks above qaf of قح.
    - Dropped the special combination in تمخـ when it is follow vowelled as
      it was too crowded.
    - Fixed the position of sukun over shadda.
    - Fixed the side bearings of ثر, ثن and sisters so that the dots do not clash
      with preceding glyphs.
    - Positive kerning between مرين and likes.
    - Slight kerning between the period and closing quotes.
    - Made sure the italic European digits are really tabular.

Amiri 0.106 (2013-05-28)
------------------------
* New glyphs:
    - New, more conventional shape for gaf, the old shape can be activated with
      `ss04` feature.
    - Redrawn Persian digits
    - New inverted damma, the old one moved to Urdu-specific `locl` feature.
    - More contextual forms for letter followed by final bari yeh.

* Fixes:
    - Add +ve kerning after alef in أثر and أثن.
    - Cleanup some bold glyphs.
    - Fix ring position of few U+0620 glyphs.
    - Lower the marks above wide isolated glyphs.
    - Rewrite subtending marks lookups to become much faster.
    - Shorten final Alef with tatweel a bit.
    - Bigger quotes.
    - Increase slant angle of slanted font.
    - Use medium sized digits with safha and number signs instead of small ones.
    - Many smaller changes.

* Latin:
    - Remove the tooth from italic longs.

* License
    - Drop the OFL reserved font name clause; no need to rename the font when
      modifying it anymore.

* A draft user manual (Arabic only for now) is included.

Amiri 0.105 (2012-12-31)
------------------------
* New Quran font:

  This release features a new separate Amiri Quran font for typesetting Quran.

  It is basically a subset of Amiri Regular font with some default settings and
  features tailored for Quran typesetting requirements that are not suitable
  for general text. For example:
    - Covers only the subset of characters required for Quran.
    - Bigger line height to accommodate waqf marks.
    - Hamza on yeh or waw when followed by kasra is placed bellow its base.
    - Supports overline mark (U+0305) that can be used to draw sajda lines in
      situations where proper overline formating is not available.
    - The Allah ligature is always active, no checking for surrounding letters or
      vowel marks, also no automatic insertion of shadda above it.
    - Some ligatures that are problematic for fully vowelled text are disabled.

* Lots of metrics, mark positioning, kerning and glyph shape tuning. Check GIT
  log for complete list.

Amiri 0.104 (2012-07-19)
------------------------
* New glyphs:
    - New localised slash glyph, to align better with Arabic digits.
    - New, less bulky Arabic @ sign.
    - Proportional digits (`pnum` feature).

* Fixes:
    - Give some room to the low small waw.
    - Fix seen tooth with `ss02`.
    - Fix raa with inverted v above.
    - Improve medial kaf of kaf-mem-alef
    - Make subtending marks work with Firefox (and other HarfBuzz based
      applications).
    - Arabic number sign (U+0600) now accepts a 4th digits, and is made a bit
      wider, to avoid collision with wide digits.
    - Fix combining Qur’anic madda with inverted damma.
    - Drop the Th ligature.
    - Other miscellaneous fixes.

* Kerning:
    - Kern final lam-alef with kaf.

Amiri 0.103 (2012-05-31)
------------------------
* This is a bug fix release:
    - Fix wrong kerning of digits inside end of ayah and other Arabic enclosing
      marks.
    - Add visible glyphs for BiDi control characters.
    - Kern more kaf forms accross ZWNJ.
    - Fix handling of right-slanting and left-slanting common characters in the
      italic fonts to be more logical.

Amiri 0.102 (2012-05-22)
------------------------
* New glyphs:
    - The largest feature of this release is adding Latin script support based on
      Crimson font, covering latin-0 to 9 code pages as well as all characters
      used in common Arabic romanisation schemes (no including IPA) and other
      common punctuation characters.
    - Beh with small v below (U+08A0).
    - Basmala symbol (U+FDFD).

* Fixes:
    - New contextual shape for final open heh-yaa combination.
    - New contextual shape for final faa-yaa combination.
    - New contextual shape for knotted heh-yaa baree.
    - New, improved and more open hmaza wasl.
    - Larger and more readable shadda, regular and Qur’anic sukun.
    - Larger and more readable Sallallahou Alayhe Wasallam symbol (U+FDFA).
    - Improved dot placement of initial baa-like glyphs.
    - Improved dot placement of kaf-baa-alef combination.
    - Improved placement of dagger alef on regular glyphs.
    - Wider final alef with madda to avoid clash between madda and next glyphs.
    - Improved kaf-meem-alef, kaf-alef combinations at smaller sizes on screen.
    - Improve kaf-lam-final meem.
    - Avoid initial/medial kaf clash with next glyph’s dots.
    - Improved medial and final sad connecting part.

* Kerning:
    - More efficient kerning feature using contextual positioning
    - Reduce dal/raa-kaf kerning to avoid dot clash
    - More positive kerning for raa-intial yaa.
    - Make kerning across ZWNJ work with Uniscribe.

* Bug fixes: #1347860, #3471042, #3475146, #3509875

* Misc.:
    - Duplicate `locl` in `ccmp` to work around engines not supporting the former.
    - Smaller, MTX compressed EOT files.

* Many other subtle improvements here and there.

Amiri 0.101 (2011-12-27)
------------------------
* New styles:
    - This release features a bold font that is, though not as polished as the
      regular one, quite usable.
    - Bold Slanted font.

* New glyphs:
    - Sallallahou Alayhe Wasallam symbol (U+FDFD).
    - Ornate parenthesis (U+FD3E, U+FD3F).
    - Arabic pedagogical symbols (U+FBB2-U+FBC1).
    - Most of Presentation Forms-A and B blocks.

* Fixes:
    - Fix misplaced Yaa dots on some Apple applications.
    - Enable local period and guillemots for Urdu and Sindhi languages.
    - Fix disabled mark and curs features with Urdu and Sindhi languages.
    - Fix wrong Baa when followed by Seen then Heh, as in بسهل.
    - Fix some misplaced dots.
    - Fix Hamza placement above final Heh.
    - Widen final Alef to be less acute and avoid touching adjacent glyphs.
    - Fix clash of medial Lam mark and final Yaa dots, as in هلِي.
    - Support European digits with subtending marks.
    - Use larger digits with the year sign to be more usable.
    - Prevent double high Baa when preceded and followed by Seen, as in سببس.

Amiri 0.100 (2011-12-04), beta gamma delta
------------------------------------------
* This release marks another important developmental milestone, with Arabic and
  Arabic Supplement blocks in Unicode 6.0 being fully covered (which means
  essentially any Arabic character in Unicode can now be presented with Amiri).
  Also the font has now matured to great extent and is usable for most of
  typesetting tasks.

* New styles:
    - Add a slanted style that slants to the left and no to right, to follow
      Arabic writing direction.

* New glyphs:
    - Subtending marks (U+0600-0603).
    - Arabic date separator (U+060D).
    - Arabic poetic verse sign (U+060E).
    - Honorific marks (U+0610-0614).
    - Dochashmi Heh (U+06BE and U+06FF).
    - Bari Yaa (U+06D2 and U+06D3).
    - 4 sizes of Kashida.

* Fixes:
    - Fix issue with Kashida breaking word shaping in InDesign.
    - Slant Urdu digit four to look more acceptable.
    - Fix disappearance of media Khaa dot when preceded by Kaf, as in كخا.
    - Decrease the hight of initial Lam when followed by Haa and Meem, as in
      لحمد, to match other Lam glyphs.
    - Finjani Ayn and closed Haa when followed by Kaf.
    - Lower small Waw after final Heh.
    - Widen small Waw and final Alef when a Madda mark is applied to them.
    - Increase side bearings of many dotted glyphs no avoid clash with their
      neighbours.
    - More wider forms of glyphs to avoid mark clash when fully vowelled.
    - New contextual shape for initial Ain followed by Raa, as in غر.
    - New contextual shape for final Alef preceded by Kashida, as in عمـان.
    - New contextual shape for final Yaa when followed by open Heh, as in نهى.
    - New redrawn initial and medial Kaf that do not clash with their neighbours.
    - New redrawn final Waw that is more faithful to the original design.
    - Disable, by default, lowering Baa dots when preceded by Raa or Waw, moved
      to stylistic set 01.
    - Disable, by default, contextual form of medial Meem when followed by Alef,
      moved to stylistic set 02.
    - Digits are now tabular, removed tnum feature.
    - Common punctuation and European digits are now from Crimson Text.
    - Change the default interline spacing to fit better for regular text.
    - Many more smaller fixes here and there.

Amiri 0.016 (2011-09-22), Beginning of the End
----------------------------------------------
* This release features full Quranic support, another major developmental
  milestone, more work still needed in refining glyph interaction specially
  mark positioning in fully vocalised text such as Quran.

* New glyphs:
    - All Quranic annotation marks in Unicode 6.0.
    - All other Arabic vowel marks in Unicode 6.0.
    - Radical (U+221A) including a RTL variant, and other Arabic radicals
      (U+0606, U+0607).
    - Arabic ray (U+0608).
    - Afghani sign (U+060B).
    - Arabic sign Misra (U+060F).
    - New contextual shape for initial meem followed by medial heh, as in مها.

* Kerning:
    - Decreased the number of kerning pairs from 411240 to 55850 while retaining
      the same functionality.

* Fixes:
    - General cleanup of punctuation marks, fixing spacing of brackets and making
      curly brackets more bolder to fit wit the rest of the font.
    - Made the space glyph 600 units wide.
    - Fixed erroneous tatweel (kashida) insertion in full justification.
    - Wider forms of some glyphs to avoid mark clash when fully vowelled.
    - Underline position is now lower than most glyphs with descendants.
    - Various mark positioning fixes.
    - Separate the ring of Kashmiri yeh from the body of base glyph, following
      Kashmiri orthographic traditions.

Amiri 0.015 (2011-07-14), Phoenix
---------------------------------
* This release represents a major developmental milestone, as the OpenType
  layout have been rewritten to allow maximum compatibility with various
  OpenType implementations.

* Cleanup:
    - More unification and tidy up.
    - Various fixes for FontForge warnings.
    - Various dot placement fixes.
    - Various tashkil fine tuning.
    - Fixes to Lellah form.
    - Fine tune initial Baa/final Alef combination.

* More kerning pairs.

* Font name is now shown only in English in font menus.

Amiri 0.014 (2011-06-05), Break a Leg
-------------------------------------
* Another minor release to fix two bugs:
    - Lellah bug on Windows and MS Office.
    - Wrong placement of dots under final Yaa.

Amiri 0.013 (2011-04-27), Hurry up!
-----------------------------------
* A minor release to fix mark positioning on kerned glyphs in Windows.

Amiri 0.012 (2011-04-26), A Long Night
--------------------------------------

* New glyphs:
    - Add localised Urdu and Sindhi digits (`locl` feature).
    - Add tabular numbers feature (`tnum`).
    - European numbers and some punctuation marks from Linux Libertine.
    - Add at sign with experimental Arabic variant (`locl` feature, too).
    - Add triple dot punctuation mark (U+061E).
    - Add middle dot (U+00B7).
    - Reimplement الله igature properly and added فلله ligature; the code now
      much more careful on when to activate this ligature.


* Cleanup:
    - Massive cleanup removing tens of too similar glyphs, making the font more
      unified and consistent.
    - This cleanup results in more contextual variants that were missing before,
      yet the font is smaller not larger.
    - Scaled Tashkil marks down by 80%, they are now smaller leading too less
      mark collision.
    - The Arabic digits are more polished.
    - Misc. mark fixes.
    - Less use of exotic OpenType features to work with even more OpenType
      implementations.

* More kerning pairs.

* Bug fixes: 3234138, 3110760, 3087332, 3073139, 3211187, 3211239 and 3078741

Amiri 0.011 (2011-03-31), Inflating the Tire
--------------------------------------------

* New glyphs:
    - `"#'*,-/;[\]{|}¦`
    - Single and double angle quotation marks: `‹›«»`, in addition to rounded
      Arabic variant.
    - Curly quotation marks: `‟„”“‛‚’‘`
    - Asterism symbol: `⁂`
    - Fraction slash: `⁄`
    - Arabic percent signs: `٪؊؉`
    - Arabic decimal and thousands separators: `٫٬`
    - Arabic five pointed star: `٭`
    - Typographic dashes: `‒ – — ―`
    - Proper support for Arabic characters with traverse stroke: `ۅ ݛ ݪ`
    - Arabic characters with digit marks: `ݳ ݴ ݵ ݶ ݷ ݸ ݹ ݼ ݽ`

* Misc. fixes:
    - Update font metadata.
    - Scale all numbers by 120% since they were drawn smaller than what they
      should, and raise them a bit.
    - Misc. cleanup of punctuation and math glyphs.
    - Proper mark support for standalone Hamza.
    - Visually centralise marks bellow isolated Heh.

Amiri 0.010 (2011-03-21), Referendum
------------------------------------

* New glyphs:
    - Lam with three dots below (U+06B8).

* Kerning:
    - Lam of له with preceding Raa/Waw family.
    - Kaf of كتب as well.

* Glyph fixes:
    - Fixed exclamation mark’s vertical position as compared to question mark.
    - Removed stray Hamza from U+063B and U+063C initial and medial forms.
    - Fixed the weight of isolated Dal, was much bolder than the rest of the font.
    - Fixed Lam Meem connection in لما, there was a slight mismatch.
    - Fixed the size of medial Ayn compared to the head of final one.

* OpenType code:
    - Removed DFLT script from `locl` feature which would cause it to be on
      unconditionally.
    - Got rid of mark sets in favour of the more widely supported mark classes.

Amiri 0.009 (2011-02-06), Revolution
------------------------------------

* New glyphs:
    - Initial support for vowel marks, still needs more adjustments and fine
      tuning.
    - Arabic and Persian digits.
    - More punctuation marks.
    - More coverage of extended Arabic characters.
    - More glyph variants, especially for pairs ending with Haa.

* Attempted to get around OOo bugs, it should render much better now. A proper
  fix have been submitted to LibreOffice developers but didn’t make it into
  3.3.0 release.
* Packed sfdir into an sfd file in the release, should make it easier for
  others to open the source in FontForge.
* Increased line spacing a bit to give more room for vowel marks.
* More coverage and kerning fixes.
* Tens of other small fixes here and there.

* Bug fixes:
    - 3085159 Kaf clashes with next letters
    - 3085165 Hamza on Alef clashes wit next and previous letters
    - 3085166 Raa and Zay clashes with next Yaa
    - 3085172 Kaf clashes with next Lam-Meem combination
    - 3085174 Lam-Alef is broken of preceded by Kaf-Meem
    - 3085175 Succeeding Haa clash with each other
    - 3101634 Missing kerning
    - 3101674 Finjani Ayn

Amiri 0.003 (2010-10-10)
-----------------------

* More tuning of kerning, especially handling of dot clash between
  kerned glyphs.
* Resolved many glyph clashes especially between ل and ك, between ك and
  letters with above dots after it, and between marks of ب and ا.
* Persian should be now fully supported, other languages to follow.

Amiri 0.002 (2010-09-25)
-----------------------

* More kerning work:

  Kerning have been further refined, extended in coverage especially
  between contextual variants, and mysterious dot movements on Windows
  resulting from bad interaction between kerning and dot positioning
  have been fixed.

* Refined dot positioning:

  Some dot placements have been refined, though this area still in need
  of more work.

* Smaller file size:

  The uncompressed TTF file is now approximately 25% smaller than previous
  release, saving a bit more bandwidth when used as web font.

Amiri 0.001 (2010-9-19)
-----------------------

First release.

