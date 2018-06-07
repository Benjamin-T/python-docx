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

    def __getitem__(self, idx):
        """Provides list like access to the bookmarks """
        bookmarkStart = self._bookmarkStarts[idx]
        return Bookmark(bookmarkStart)

    def __len__(self):
        """
        Returns the total count of ``<w:bookmarkStart>`` elements in the
        document
        """
        return len(self._bookmarkStarts)

    @property
    def _bookmarkStarts(self):
        return self._document.xpath('.//w:bookmarkStart')


class Bookmark(ElementProxy):
    """
    The :class:`Bookmark` object is an proxy element which is used to wrap
    around the xml elements ``<w:bookmarkStart>`` and ``<w:bookmarkEnd>``
    """

    def __init__(self, doc_element):
        super(Bookmark, self).__init__(doc_element)
        self._element = doc_element

    @property
    def name(self):
        """ Returns the element's name."""
        return self._element.name

    @property
    def id(self):
        """ Returns the element's unique identifier."""
        return self._element.bmrk_id

    @property
    def is_closed(self):
        """ If True, the bookmark is closed. """
        return self._element.is_closed

    @property
    def _next_id(self):
        """ If True, the bookmark is closed. """
        return self._element._next_id
