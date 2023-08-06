# -*- coding: utf-8 -*-

DATA_SET = [
    # normal paragraph
    (  # 0
        [u"*first line*"],

        [u"<span class=notranslate>*first line*</span>\n"]
    ),
    (  # 1
        [u"first line",
         u"**second line**"],

        [u"first line <span class=notranslate>**second line**</span>\n"]
    ),
    (  # 2
        [u"first line",
         u"second line",
         u"``third line``"],

        [u"first line second line "\
         u"<span class=notranslate>``third line``</span>\n"]
    ),
    (  # 3
        [u"first line",
         u"  **second line**"],

        [u"first line\n",
         u"  <span class=notranslate>**second line**</span>\n"]
    ),
    (  # 4
        [u"first line",
         u"  second line",
         u"    ``third line``"],

        [u"first line\n",
         u"  second line\n",
         u"    <span class=notranslate>``third line``</span>\n"]
    ),
    (  # 5
        [u"first line",
         u"  second line",
         u"    third line",
         u"  fourth line"],

        [u"first line\n",
         u"  second line\n",
         u"    third line\n",
         u"  fourth line\n"],
    ),
    (   # 6
        # auto line break with textwrap
        [u"long long long long long long long long long long first line",
         u"looooooooooooooooooooooooooooooooooooooooong **second line**"],

        [u"long long long long long long long long long long first line\n"\
          "looooooooooooooooooooooooooooooooooooooooong <span\n"\
          "class=notranslate>**second line**</span>\n"]
    ),
    (   # 7
        # role
        [u":mod:`ikazuchi` has some functions, ",
         u":func:`translate` and :func:`detect`."],

        [u"<span class=notranslate>:mod:`ikazuchi`</span> has some "\
         u"functions,\n<span class=notranslate>:func:`translate`</span> "\
         u"and <span\nclass=notranslate>:func:`detect`</span>.\n"]
    ),

    # paragraph with indent
    (  # 8
        [u"  *first line*"],

        [u"  <span class=notranslate>*first line*</span>\n"]
    ),
    (  # 9
        [u"  first line",
         u"  **second line**"],

        [u"  first line <span class=notranslate>**second line**</span>\n"]
    ),
    (  # 10
        [u"  first line",
         u"  second line",
         u"  ``third line``"],

        [u"  first line second line "\
         u"<span class=notranslate>``third line``</span>\n"]
    ),
    (  # 11
        [u"  first line",
         u"    **second line**"],

        [u"  first line\n",
         u"    <span class=notranslate>**second line**</span>\n"]
    ),
    (  # 12
        [u"  first line",
         u"    second line",
         u"      ``third line``"],

        [u"  first line\n",
         u"    second line\n",
         u"      <span class=notranslate>``third line``</span>\n"]
    ),
    (  # 13
        [u"  first line",
         u"    second line",
         u"      third line",
         u"    fourth line"],

        [u"  first line\n",
         u"    second line\n",
         u"      third line\n",
         u"    fourth line\n"],
    ),
    (   # 14
        # auto line break with textwrap
        [u"  long long long long long long long long long long first line",
         u"  looooooooooooooooooooooooooooooooooooooooong **second line**"],

        [u"  long long long long long long long long long long first line\n"\
          "  looooooooooooooooooooooooooooooooooooooooong <span\n"\
          "  class=notranslate>**second line**</span>\n"]
    ),
    (   # 15
        # role
        [u"  :mod:`ikazuchi` has some functions, ",
         u"  :func:`translate` and :func:`detect`."],

        [u"  <span class=notranslate>:mod:`ikazuchi`</span> has some "\
         u"functions,\n  <span class=notranslate>:func:`translate`</span> "\
         u"and <span\n  class=notranslate>:func:`detect`</span>.\n"]
    ),
]
