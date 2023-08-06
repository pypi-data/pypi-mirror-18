# -*- coding: utf-8 -*-

DATA_SET = [
    (   # 0 no indent line
         u"no indent line.",

        [u"no indent line.\n"],
    ),
    (   # 1 indent line
         u"  indent line.",

        [u"  indent line.\n"],
    ),
    (   # 2 no indent long line
         u"no indent long long long long long long long long long long "\
         u"long long long long long long long long long long long long "\
         u"long long long long line.",

        [u"no indent long long long long long long long long long long "\
         u"long long\nlong long long long long long long long long long "\
         u"long long long long\nline.\n"]
    ),
    (   # 3 indent long line
         u"  indent long long long long long long long long long long "\
         u"long long long long long long long long long long long long "\
         u"long long long long line.",

        [u"  indent long long long long long long long long long long "\
         u"long long\n  long long long long long long long long long long "\
         u"long long long\n  long line.\n"]
    ),
]
