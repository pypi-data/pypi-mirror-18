from __future__ import absolute_import, unicode_literals

import sys


def message(text):
    sys.stdout.write('{}\n'.format(text))
