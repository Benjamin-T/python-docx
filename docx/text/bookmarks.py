# encoding: utf-8

"""
Bookmarks-related proxy types.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import Sequence

from docx.shared import ElementProxy


class Bookmarks(Sequence):
    def __init__(self, document_elm):
        super(Bookmarks, self).__init__()
        self._document = self._element = document_elm
