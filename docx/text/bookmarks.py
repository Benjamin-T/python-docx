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

    def __iter__(self):
        """Enables list like iteration of the bookmark starts. """
        for bookmarkStart in self._bookmarkStarts:
            yield Bookmark(bookmarkStart)

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

    def get(self, name, default=None):
        """
        Get method which returns the bookmark corresponding to the name
        provided.
        """
        for bookmarkStart in self._bookmarkStarts:
            if bookmarkStart.name == name:
                return Bookmark(bookmarkStart)
        return default

    @property
    def _bookmarkStarts(self):
        """Returns a list of ``<w:bookmarkStart>`` elements """
        return self._document.xpath('.//w:bookmarkStart')

    @property
    def _bookmarkEnds(self):
        """Returns a list of ``<w:bookmarkEnd>`` elements """
        return self._document.xpath('.//w:bookmarkEnd')


class Bookmark(ElementProxy):
    """
    The :class:`Bookmark` object is an proxy element which is used to wrap
    around the xml elements ``<w:bookmarkStart>`` and ``<w:bookmarkEnd>``
    """
    def __init__(self, doc_element):
        super(Bookmark, self).__init__(doc_element)
        self._element = doc_element

    @property
    def id(self):
        """ Returns the element's unique identifier."""
        return self._element.bmrk_id

    @property
    def name(self):
        """ Returns the element's name."""
        return self._element.name

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
    def start_bookmark(self, name):
        """
        The :func:`start_bookmark` method is used to place the start of  a
        bookmark. It requires a name as input.

        :param str name: Bookmark name

        """
        bookmarkstart = self._element._add_bookmarkStart()
        bookmarkstart.bmrk_id = bookmarkstart._next_id
        bookmarkstart.name = name
        return Bookmark(bookmarkstart)

    def end_bookmark(self, bookmark=None):
        """
        The :func:`end_bookmark` method is used to end a bookmark. It takes a
        :any:`Bookmark<docx.text.bookmarks.Bookmark>` as optional input.

        """
        bookmarkend = self._element._add_bookmarkEnd()
        if bookmark is None:
            bookmarkend.bmrk_id = bookmarkend._next_id
            if bookmarkend.is_closed:
                raise ValueError('Cannot end closed bookmark.')
        else:
            if bookmark.is_closed:
                raise ValueError('Cannot end closed bookmark.')
            bookmarkend.bmrk_id = bookmark.id
        return Bookmark(bookmarkend)
