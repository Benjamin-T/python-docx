# encoding: utf-8

"""Objects related to bookmarks."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import Sequence
from itertools import chain

from docx.oxml.ns import qn
from docx.shared import lazyproperty
from docx.oxml.xmlchemy import ZeroOrMore
from docx.oxml.bookmark import CT_MarkupRange

class BookmarkParent(object):
    """
    The :class:`BookmarkParent` object is used as mixin object for the
    different parts of the document. It contains the methods which can be used
    to start and end a Bookmark.
    """
    bookmarkStart = ZeroOrMore('w:bookmarkStart')
    bookmarkEnd = ZeroOrMore('w:bookmarkEnd')

    def start_bookmark(self, name):
        """
        The :func:`start_bookmark` method is used to place the start of  a
        bookmark. It requires a name as input.

        :param str name: Bookmark name

        """
        bookmarks = Bookmarks(self.part)
        names = [bookmark.name for bookmark in bookmarks]

        if name not in names:
            bmk_id = bookmarks.next_id
            bookmarkstart = self._element._add_bookmarkStart()
            bookmarkstart.name = name
            bookmarkstart.id = bmk_id
        else:
            raise KeyError('Bookmark name already present in document.')

        return _Bookmark((bookmarkstart, None))

    def end_bookmark(self, bookmark):
        """
        The :func:`end_bookmark` method is used to end a bookmark. It takes a
        :any:`Bookmark<docx.text.bookmarks.Bookmark>` as input.

        :param obj bookmark: Bookmark object that needs an end.

        """
        bookmarkend = self._element._add_bookmarkEnd()
        bookmarkend.id = bookmark.id
        bookmark._bookmarkEnd = bookmarkend
        return bookmark


class Bookmarks(Sequence):
    """Sequence of |Bookmark| objects."""

    def __init__(self, document_part):
        self._document_part = document_part

    def __getitem__(self, idx):
        bookmark_pair = self._finder.bookmark_pairs[idx]
        return _Bookmark(bookmark_pair)

    def __iter__(self):
        # ---not strictly required, but improves performance over default
        # ---implementation that makes repeated calls to __getitem__()
        return (_Bookmark(pair) for pair in self._finder.bookmark_pairs)

    def __len__(self):
        return len(self._finder.bookmark_pairs)

    def get(self, name=None):
        """Get bookmark based on its bookmark name."""
        for bookmark in self:
            if bookmark.name == name:
                return bookmark

    def get_by_id(self, id=None):
        """Get bookmark based on its unique id."""
        for bookmark in self:
            if bookmark.id == id:
                return bookmark

    @lazyproperty
    def _finder(self):
        """_DocumentBookmarkFinder instance for this document."""
        return _DocumentBookmarkFinder(self._document_part)

    @property
    def next_id(self):
        return len(list(self._finder.bookmark_starts)) + 1


class _Bookmark(object):
    """Proxy for a (w:bookmarkStart, w:bookmarkEnd) element pair."""

    def __init__(self, bookmark_pair):
        self._bookmarkStart, self._bookmarkEnd = bookmark_pair

    @property
    def id(self):
        return self._bookmarkStart.id

    @property
    def name(self):
        return self._bookmarkStart.name

    @name.setter
    def name(self, name):
        self._bookmarkStart.name = name

    @property
    def bookmark_text(self):
        xpath = '//w:bookmarkStart[@w:id=%s]/following::w:t[following::w:bookmarkEnd[@w:id=%s]]' % (self.id, self.id)
        bookmark_xpath = self._bookmarkEnd.xpath(xpath)
        from docx.text.run import Run
        return [Run(run, None).text for run in bookmark_xpath if len(bookmark_xpath) > 0]


class _DocumentBookmarkFinder(object):
    """Provides access to bookmark oxml elements in an overall document."""

    def __init__(self, document_part):
        self._document_part = document_part

    @property
    def bookmark_pairs(self):
        """List of (bookmarkStart, bookmarkEnd) element pairs for document.

        The return value is a list of two-tuples (pairs) each containing
        a start and its matching end element.

        All story parts of the document are searched, including the main
        document story, headers, footers, footnotes, and endnotes. The order
        of part searching is not guaranteed, but bookmarks appear in document
        order within a particular part. Only well-formed bookmarks appear.
        Any open bookmarks (start but no end), reversed bookmarks (end before
        start), or duplicate (name same as prior bookmark) bookmarks are
        ignored.
        """
        return list(
            chain(*(
                _PartBookmarkFinder.iter_start_end_pairs(part)
                for part in self._document_part.iter_story_parts()
            ))
        )

    @property
    def bookmark_starts(self):
        return list(
            chain(*(
                _PartBookmarkFinder.iter_starts(part)
                for part in self._document_part.iter_story_parts()
            ))
        )


class _PartBookmarkFinder(object):
    """Provides access to bookmark oxml elements in a story part."""

    def __init__(self, part):
        self._part = part

    @classmethod
    def iter_start_end_pairs(cls, part):
        """Generate each (bookmarkStart, bookmarkEnd) in *part*."""
        return cls(part)._iter_start_end_pairs()

    @classmethod
    def iter_starts(cls, part):
        return cls(part)._iter_starts()

    def _iter_start_end_pairs(self):
        """Generate each (bookmarkStart, bookmarkEnd) in this part."""
        for idx, bookmarkStart in self._iter_starts():
            # ---skip open pairs---
            bookmarkEnd = self._matching_end(bookmarkStart, idx)
            if bookmarkEnd is None:
                continue
            # ---skip duplicate names---
            if not self._add_to_names_so_far(bookmarkStart.name):
                continue
            yield (bookmarkStart, bookmarkEnd)

    def _iter_starts(self):
        """Generate (idx, bookmarkStart) elements in story.

        The *idx* value indicates the location of the bookmarkStart element
        among all the bookmarkStart and bookmarkEnd elements in the story.
        """
        for idx, element in enumerate(self._all_starts_and_ends):
            if element.tag == qn('w:bookmarkStart'):
                yield idx, element

    @lazyproperty
    def _all_starts_and_ends(self):
        return self._part.element.xpath('//w:bookmarkStart|//w:bookmarkEnd')

    def _matching_end(self, bookmarkStart, idx):
        for element in self._all_starts_and_ends[idx + 1:]:
            # ---skip bookmark starts---
            if element.tag == qn('w:bookmarkStart'):
                continue
            bookmarkEnd = element
            if bookmarkEnd.id == bookmarkStart.id:
                return bookmarkEnd
        return None

    def _add_to_names_so_far(self, name):
        """Return True if name was added, False if name already present."""
        names_so_far = self._names_so_far
        if name in names_so_far:
            return False
        names_so_far.add(name)
        return True

    @lazyproperty
    def _names_so_far(self):
        return set()
