# encoding: utf-8

"""
Test suite for the docx.text.bookmarks module, containing the Bookmarks and
Bookmark objects.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

from docx.text.bookmarks import Bookmark, Bookmarks

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock


class DescribeBookmarks(object):

    def it_knows_its_length(self, len_fixture):
        bookmarks, expected_value = len_fixture
        assert len(bookmarks) == expected_value

    def it_can_get_a_bookmark_by_index(self, index_fixture):
        bookmarks, idx, Bookmark_, bookmark, bookmark_ = index_fixture
        bookmark = bookmarks[idx]
        assert bookmark is bookmark_

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:p',                                          0),
        ('w:p/w:bookmarkStart',                          1),
        ('w:p/w:bookmarkStart/w:bookmarkStart',          2),
    ])
    def len_fixture(self, request):
        bookmarks_cxml, expected_value = request.param
        bookmarks = Bookmarks(element(bookmarks_cxml))
        return bookmarks, expected_value

    @pytest.fixture(params=[
        ('w:p/w:bookmarkStart',                          0),
        ('w:p/w:bookmarkStart/w:bookmarkStart',          1),
    ])
    def index_fixture(self, request, Bookmark_, bookmark_):
        bookmarks_cxml, idx = request.param
        p = element(bookmarks_cxml)
        bookmark = p.xpath('.//w:bookmarkStart')[idx]
        bookmarks = Bookmarks(p)
        return bookmarks, idx, Bookmark_, bookmark, bookmark_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Bookmark_(self, request, bookmark_):
        return class_mock(
            request, 'docx.text.bookmarks.Bookmark', return_value=bookmark_
        )

    @pytest.fixture
    def bookmark_(self, request):
        return instance_mock(request, Bookmark)


class DescribeBookmark(object):

    def it_has_a_name(self, bookmark_name_fixture):
        bookmark, name = bookmark_name_fixture
        assert isinstance(bookmark, Bookmark)
        assert bookmark.name == name

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:bookmarkStart{w:name=bookmark-name}',  'bookmark-name'),
    ])
    def bookmark_name_fixture(self, request):
        bookmark_cxml, name = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        return bookmark, name

    # fixture components ---------------------------------------------
