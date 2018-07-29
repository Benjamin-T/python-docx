# encoding: utf-8

"""
Bookmarks-related proxy types.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import Sequence

from docx.oxml.xmlchemy import ZeroOrMore
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
        return self._element.id

    @property
    def is_closed(self):
        """ If True, the bookmark is closed. """
        return self._element.is_closed


class BookmarkParent(object):
    """
    The :class:`BookmarkParent` object is used as mixin object for the
    different parts of the document. It contains the methods which can be used
    to start and end a Bookmark.
    """
    bookmarkStart = ZeroOrMore('w:bookmarkStart', successors=('w:sectPr',))
    bookmarkEnd = ZeroOrMore('w:bookmarkEnd', successors=('w:sectPr',))

    def start_bookmark(self, name):
        """
        The :func:`start_bookmark` method is used to place the start of  a
        bookmark. It requires a name as input.

        :param str name: Bookmark name

        """
        bookmarkstart = self._element._add_bookmarkStart()
        bookmarkstart.add_name(name)
        self._element.append(bookmarkstart)
        return Bookmark(bookmarkstart)

    def end_bookmark(self, bookmark=None):
        """
        The :func:`end_bookmark` method is used to end a bookmark. It takes a
        :any:`Bookmark<docx.text.bookmarks.Bookmark>` as optional input.

        """
        bookmarkend = self._element._add_bookmarkEnd()
        if bookmark is None:
            bookmarkend.id = bookmarkend._next_id
            if bookmarkend.is_closed:
                raise ValueError('Cannot end closed bookmark.')
        else:
            if bookmark.is_closed:
                raise ValueError('Cannot end closed bookmark.')
            bookmarkend.id = bookmark.id
        return Bookmark(bookmarkend)
