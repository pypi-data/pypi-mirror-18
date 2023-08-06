# -*- coding: utf-8 -*-

DATA_SET = [
    # standalone sourceblock
    (  # 0
        [u"::\n"
         u"",
         u"    first code",
         u"    second code",
         u""],
        u"::\n",

        [u"::\n",
         u"    first code",
         u"    second code",
         u""]
    ),
    (  # 1
        [u"::\n"
         u"",
         u"    first code",
         u"    second code"],
        u"::\n",

        [u"::\n",
         u"    first code",
         u"    second code"]
    ),
    (  # 2
        [u"::\n"
         u"",
         u"",
         u"    first code",
         u"    second code"],
        u"::\n",

        [u"::\n"
         u"",
         u"",
         u"    first code",
         u"    second code"]
    ),
    (  # 3
        [u"::  \n"
         u"",
         u"    first code",
         u"    second code",
         u""],
        u"::  \n",

        [u"::  \n",
         u"    first code",
         u"    second code",
         u""]
    ),
    (  # 4
        [u"::\n"
         u"    first code",
         u"    second code",
         u""],
        u"::\n",

        [u"::\n    first code",
         u"    second code",
         u""]
    ),

    # given first line has "::" and test
    (  # 5
        [u"that is::\n"
         u"",
         u"    first code",
         u"    second code",
         u""],
        u"that is::\n",

        [u"that is<span class=notranslate>::</span>\n",
         u"    first code",
         u"    second code",
         u""]
    ),
    (  # 6
        [u"that is::\n"
         u"",
         u"    first code",
         u"    second code"],
        u"that is::\n",

        [u"that is<span class=notranslate>::</span>\n",
         u"    first code",
         u"    second code"]
    ),
    (  # 7
        [u"that is::\n"
         u"",
         u"",
         u"    first code",
         u"    second code"],
        u"that is::\n",

        [u"that is<span class=notranslate>::</span>\n",
         u"",
         u"    first code",
         u"    second code"]
    ),
    (  # 8
        [u"that is::  \n"
         u"",
         u"    first code",
         u"    second code",
         u""],
        u"that is::  \n",

        [u"that is<span class=notranslate>::  </span>\n",
         u"    first code",
         u"    second code",
         u""]
    ),
    (  # 9
        [u"that is::\n",
         u"    first code",
         u"    second code",
         u""],
        u"that is::\n",

        [u"that is<span class=notranslate>::</span>\n",
         u"    first code",
         u"    second code",
         u""]
    ),
]
