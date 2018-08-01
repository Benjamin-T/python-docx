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
from docx.text.run import Run
from docx.document import Document, _Body

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
        assert bookmark.id == 1
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
        ('w:bookmarkStart{w:id=1}',  1),
        ('w:bookmarkEnd{w:id=1}',  1),
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
        ('w:bookmarkStart{w:id=0}', 1),
        ('w:bookmarkStart{w:id=2}', 1),
        ('w:bookmarkStart{w:id=3}/w:bookmarkStart{w:id=1}', 2),
    ])
    def bookmarks_next_id_fixture(self, request, iterancestor_):
        bookmark_cxml, expected_id = request.param
        bookmark = Bookmark(element(bookmark_cxml))
        iterancestor_.return_value = [CT_P(element(bookmark_cxml))]
        return bookmark, expected_id

    @pytest.fixture
    def bookmark_add_name_fixture(self, request, next_id_):
        next_id_.return_value = 1
        bookmark = element('w:bookmarkStart')
        return bookmark, next_id_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def iterancestor_(self, request):
        return method_mock(request, CT_Bookmark, 'iterancestors')

    @pytest.fixture
    def next_id_(self, request):
        return property_mock(request, CT_Bookmark, '_next_id')


class DescribeBookmarkParent(object):

    def it_can_start_a_bookmark(self, start_bookmark_fixture):
        paragraph, name_, expected_name, expected_id = start_bookmark_fixture
        bookmark = paragraph.start_bookmark(name=name_)
        assert bookmark.name == expected_name
        assert bookmark.id == expected_id

    def it_can_start_a_bookmark_document(self, start_bookmark_fixture_doc):
        document, bmrk_name, bookmark_, paragraph_ = start_bookmark_fixture_doc
        bookmark = document.start_bookmark(name=bmrk_name)
        assert bookmark is bookmark_
        paragraph_.start_bookmark.assert_called_once_with(bmrk_name)

    def it_can_start_a_bookmark_run(self, start_bookmark_fixture_run):
        run, bmrk_name, expected_name, expected_id = start_bookmark_fixture_run
        bookmark = run.start_bookmark(name=bmrk_name)
        assert bookmark.name == expected_name
        assert bookmark.id == expected_id

    def it_can_end_a_bookmark(self, end_bookmark_fixture):
        paragraph, bookmark_, bmrk_end_id = end_bookmark_fixture
        bookmark_end = paragraph.end_bookmark(bookmark_)
        assert bookmark_.name == 'test'
        assert bookmark_end.id == bmrk_end_id
        assert isinstance(bookmark_end, Bookmark)


    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:p', 1),
        ('w:p/w:bookmarkStart{w:id=2}', 1),
        ('w:p/w:bookmarkStart{w:id=1}/w:bookmarkStart{w:id=2}', 3),
    ])
    def start_bookmark_fixture(self, request):
        parent, expected_id = request.param
        paragraph = Paragraph(element(parent), None)
        bookmark_name = 'test_bookmark'
        expected_name = 'test_bookmark'
        return paragraph, bookmark_name, expected_name, expected_id

    @pytest.fixture
    def start_bookmark_fixture_doc(self, paragraph_, body_prop_, bookmark_):
        document = Document(None, None)
        paragraph_.start_bookmark.return_value = bookmark_
        body_prop_.return_value.add_paragraph.return_value = paragraph_
        bookmark_name = 'test_bookmark'
        return document, bookmark_name, bookmark_, paragraph_

    @pytest.fixture(params=[
        ('w:r', 1),
        ('w:r/w:bookmarkStart{w:id=2}', 1),
        ('w:r/w:bookmarkStart{w:id=1}/w:r/w:bookmarkStart{w:id=2}', 3),
    ])
    def start_bookmark_fixture_run(self, request):
        parent, expected_id = request.param
        paragraph = Run(element(parent), None)
        bookmark_name = 'test_bookmark'
        expected_name = 'test_bookmark'
        return paragraph, bookmark_name, expected_name, expected_id

    @pytest.fixture(params=[
        ('w:p/w:bookmarkStart{w:id=1,w:name=test}',
            'w:bookmarkStart{w:id=1,w:name=test}', 1),
        ('w:p/w:bookmarkStart{w:id=1}/w:bookmarkStart{w:id=2}',
             'w:bookmarkStart{w:id=2,w:name=test}', 2),
    ])
    def end_bookmark_fixture(self, request, iterancestor_):
        parent, bmrk_el, bmrk_id = request.param
        iterancestor_.return_value = [CT_P(element("w:p"))]
        paragraph = Paragraph(element(parent), None)
        bookmark = Bookmark(element(bmrk_el))
        return paragraph, bookmark, bmrk_id

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Body_(self, request, body_):
        return class_mock(request, 'docx.document._Body', return_value=body_)

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, _Body)

    @pytest.fixture
    def paragraph_(self, request):
        return instance_mock(request, Paragraph)

    @pytest.fixture
    def bookmark_(self, request):
        return instance_mock(request, Bookmark)

    @pytest.fixture
    def body_prop_(self, request, body_):
        return property_mock(request, Document, '_body', return_value=body_)

    @pytest.fixture
    def iterancestor_(self, request):
        return method_mock(request, CT_Bookmark, 'iterancestors')
