# encoding: utf-8

"""
Test suite for the docx.text.bookmarks module, containing the Bookmarks and
Bookmark objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Twips
from docx.text.bookmarks import Bookmarks, Bookmark

import pytest

from ..unitutil.cxml import element, xml
from ..unitutil.mock import call, class_mock, instance_mock


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