# encoding: utf-8

"""
Test suite for the docx.text.bookmarks module, containing the Bookmarks and
Bookmark objects.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

from docx.oxml.bookmark import CT_Bookmark
from docx.oxml.text.paragraph import CT_P
from docx.text.bookmarks import Bookmark, Bookmarks
from docx.text.paragraph import Paragraph

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock, method_mock, property_mock


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

    def it_has_an_id(self, bookmark_id_fixture):
        bookmark, expected_id = bookmark_id_fixture
        assert isinstance(bookmark, Bookmark)
        assert bookmark.id == expected_id

    def it_has_an_closed_property(self, bookmark_status_fixture):
        bookmark, expected_status = bookmark_status_fixture
        assert isinstance(bookmark, Bookmark)
        assert bookmark.is_closed == expected_status

    def it_can_get_a_new_element_id(self, bookmarks_next_id_fixture):
        bookmark, expected_id = bookmarks_next_id_fixture
        assert isinstance(bookmark, Bookmark)
        assert bookmark._element._next_id == expected_id

    def it_can_add_a_name_to_its_element(self, bookmark_add_name_fixture):
        bookmark, next_id_ = bookmark_add_name_fixture
        bookmark.add_name('test_name')
        next_id_.assert_called_once()
        assert bookmark.id == '1'
        assert bookmark.name == 'test_name'

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:bookmarkStart{w:name=bookmark-name}',  'bookmark-name'),
    ])
    def bookmark_name_fixture(self, request):
        bookmark_cxml, name = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        return bookmark, name

    @pytest.fixture(params=[
        ('w:bookmarkStart{w:id=1}',  '1'),
        ('w:bookmarkEnd{w:id=1}',  '1'),
    ])
    def bookmark_id_fixture(self, request):
        bookmark_cxml, expected_id = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        return bookmark, expected_id

    @pytest.fixture(params=[
        ('w:bookmarkStart{w:id=1}/w:bookmarkEnd{w:id=1}', True),
        ('w:bookmarkStart{w:id=1}/w:bookmarkEnd{w:id=2}', False),
        ('w:bookmarkStart{w:id=1}', False),
    ])
    def bookmark_status_fixture(self, request, iterancestor_):
        bookmark_cxml, expected_status = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        iterancestor_.return_value = [CT_P(element(bookmark_cxml))]
        return bookmark, expected_status

    @pytest.fixture(params=[
        ('w:bookmarkStart{w:id=0}', '1'),
        ('w:bookmarkStart{w:id=2}', '1'),
        ('w:bookmarkStart{w:id=3}/w:bookmarkStart{w:id=1}', '2'),
    ])
    def bookmarks_next_id_fixture(self, request, iterancestor_):
        bookmark_cxml, expected_id = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        iterancestor_.return_value = [CT_P(element(bookmark_cxml))]
        return bookmark, expected_id

    @pytest.fixture
    def bookmark_add_name_fixture(self, request, next_id_):
        next_id_.return_value = '1'
        bookmark = element('w:bookmarkStart')
        return bookmark, next_id_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def iterancestor_(self, request):
        return method_mock(request, CT_Bookmark, 'iterancestors')

    @pytest.fixture
    def next_id_(self, request):
        return property_mock(request, CT_Bookmark, '_next_id')


