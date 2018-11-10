# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

from docx.bookmark import (Bookmarks, _DocumentBookmarkFinder,
                           _PartBookmarkFinder, _Bookmark)

from docx.opc.part import Part
from docx.oxml.bookmark import CT_MarkupRange, CT_Bookmark
from docx.parts.document import DocumentPart

from .unitutil.cxml import element
from .unitutil.mock import (call, class_mock, instance_mock, method_mock,
                            property_mock, initializer_mock)


class Describe_Bookmark(object):

    def it_serves_as_proxy_for_a_bookmark_pair(self):
        bookmark_start = element('w:bookmarkStart')
        bookmark_end = element('w:bookmarkEnd')

        proxy = _Bookmark((bookmark_start, bookmark_end))

        assert proxy._bookmarkStart is bookmark_start
        assert proxy._bookmarkEnd is bookmark_end


class DescribeBookmarks(object):

    def it_knows_how_many_bookmarks_the_document_contains(
            self, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1, 2) for _ in range(42))
        bookmarks = Bookmarks(None)

        count = len(bookmarks)

        assert count == 42

    def it_provides_access_to_bookmarks_by_idx(
            self, _Bookmark_init_, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1+idx, 2+idx) for idx in range(3))
        bookmarks = Bookmarks(None)

        bookmark = bookmarks[2]

        _Bookmark_init_.assert_called_with((3, 4))

    def it_provides_access_to_its_bookmark_finder_to_help(
            self, document_part_, _DocumentBookmarkFinder_, finder_):
        _DocumentBookmarkFinder_.return_value = finder_
        bookmarks = Bookmarks(document_part_)

        finder = bookmarks._finder

        _DocumentBookmarkFinder_.assert_called_once_with(document_part_)
        assert finder is finder_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Bookmark(self, request):
        class_mock(request, 'docx.bookmark._Bookmark')

    @pytest.fixture
    def _Bookmark_init_(self, request):
        return initializer_mock(request, _Bookmark)

    @pytest.fixture
    def _DocumentBookmarkFinder_(self, request):
        return class_mock(request, 'docx.bookmark._DocumentBookmarkFinder')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def finder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def _finder_prop_(self, request):
        return property_mock(request, Bookmarks, '_finder')


class Describe_DocumentBookmarkFinder(object):

    def it_finds_all_the_bookmark_pairs_in_the_document(
            self, pairs_fixture, _PartBookmarkFinder_):
        document_part_, calls, expected_value = pairs_fixture
        document_bookmark_finder = _DocumentBookmarkFinder(document_part_)

        bookmark_pairs = document_bookmark_finder.bookmark_pairs

        document_part_.iter_story_parts.assert_called_once_with()
        assert (
            _PartBookmarkFinder_.iter_start_end_pairs.call_args_list == calls
        )
        assert bookmark_pairs == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ([[(1, 2)]],
         [(1, 2)]),
        ([[(1, 2), (3, 4), (5, 6)]],
         [(1, 2), (3, 4), (5, 6)]),
        ([[(1, 2)], [(3, 4)], [(5, 6)]],
         [(1, 2), (3, 4), (5, 6)]),
        ([[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]],
         [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]),
    ])
    def pairs_fixture(self, request, document_part_, _PartBookmarkFinder_):
        parts_pairs, expected_value = request.param
        mock_parts = [
            instance_mock(request, Part, name='Part-%d' % idx)
            for idx, part_pairs in enumerate(parts_pairs)
        ]
        calls = [call(part_) for part_ in mock_parts]

        document_part_.iter_story_parts.return_value = (p for p in mock_parts)
        _PartBookmarkFinder_.iter_start_end_pairs.side_effect = parts_pairs

        return document_part_, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _PartBookmarkFinder_(self, request):
        return class_mock(request, 'docx.bookmark._PartBookmarkFinder')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)


class Describe_PartBookmarkFinder(object):

    def it_adds_found_bookmark_names_to_its_collection(
                                    self, _add_to_names_so_far_fixture):

        part_, _names_so_far_, expected_, name_ = _add_to_names_so_far_fixture
        _names_so_far_.return_value = {'test'}
        _partbookmarkfinder = _PartBookmarkFinder(part_)

        val = _partbookmarkfinder._add_to_names_so_far(name_)
        assert val == expected_

    def it_locates_matching_bookmark_ends(
            self, matching_bookmark_ends_fixture):
        part_, __all_starts_and_ends, bookmarkStart_, bookmarkEnd_,\
            = matching_bookmark_ends_fixture

        _partbookmarkfinder = _PartBookmarkFinder(part_)
        __all_starts_and_ends.return_value = [None, bookmarkEnd_]

        test = _partbookmarkfinder._matching_end(bookmarkStart_, 0)

        assert test is bookmarkEnd_
        assert test.id == 1
        assert isinstance(bookmarkStart_, CT_Bookmark)
        assert isinstance(bookmarkEnd_, CT_MarkupRange)

    def it_has_a_set_with_names(self, part_):
        _partbookmarkfinder = _PartBookmarkFinder(part_)
        names = _partbookmarkfinder._names_so_far
        assert isinstance(names, set)

    def it_iterates_start_end_pairs(self, iter_start_end_fixture):
        expected, part_, _iter_starts_, _matching_end_, \
           _add_to_names_so_far_, name = iter_start_end_fixture

        _partbookmarkfinder = _PartBookmarkFinder(part_)

        result = list(_partbookmarkfinder._iter_start_end_pairs())[0]

        assert result == expected
        assert isinstance(expected[0], CT_Bookmark)
        assert isinstance(expected[1], CT_MarkupRange)
        _iter_starts_.assert_called_once_with()
        _matching_end_.assert_called_once_with(expected[0], 0)
        _add_to_names_so_far_.assert_called_once_with(name)

    def it_iterates_bookmark_starts(self, __all_starts_and_ends, part_):
        exp_element = element('w:bookmarkStart')

        __all_starts_and_ends.return_value = [exp_element]
        partbookmarkfinder_ = _PartBookmarkFinder(part_)

        idx, element_ = list(partbookmarkfinder_._iter_starts())[0]
        assert idx == 0
        assert element_ == exp_element

    def it_finds_all_bookmark_starts_and_ends(self, part_element_):
        a = _PartBookmarkFinder(part_element_)
        starts_ends = a._all_starts_and_ends
        assert len(starts_ends) == 2

    def it_provides_an_iter_start_end_pairs_interface_method(
            self, part_, _init_, _iter_start_end_pairs_):

        pairs = _PartBookmarkFinder.iter_start_end_pairs(part_)

        _init_.assert_called_once_with(part_)
        _iter_start_end_pairs_.assert_called_once_with()
        assert pairs == _iter_start_end_pairs_.return_value

# fixture --------------------------------------------------------

    @pytest.fixture(params=[
            ('test', False),
            ('foo-bar', True)])
    def _add_to_names_so_far_fixture(self, request, part_, _names_so_far_):
        name_, expected_ = request.param
        return part_, _names_so_far_, expected_, name_

    @pytest.fixture
    def iter_start_end_fixture(self, request, part_, _add_to_names_so_far_,
                               _iter_starts_, _matching_end_):
        name = 'test'
        bookmark_start_ = element('w:bookmarkStart{w:name=test}')
        bookmark_end_ = element('w:bookmarkEnd')

        _iter_starts_.return_value = [(0, bookmark_start_)]
        _matching_end_.return_value = bookmark_end_
        _add_to_names_so_far_.return_value = True

        expected = (bookmark_start_, bookmark_end_)

        return expected, part_, _iter_starts_, _matching_end_,\
            _add_to_names_so_far_, name

    @pytest.fixture(params=[
        ('w:document', DocumentPart),
    ])
    def part_element_(self, request):
        part_element, part = request.param
        element_ = element('%s/w:bookmarkStart/w:bookmarkEnd' % part_element)
        return part(None, None, element_, None)

    @pytest.fixture
    def matching_bookmark_ends_fixture(self, request, part_,
                                       __all_starts_and_ends):
        bookmarkEnd_ = element('w:bookmarkEnd')
        bookmarkEnd_.id = 1

        bookmarkStart_ = element('w:bookmarkStart')
        bookmarkStart_.id = 1

        return part_, __all_starts_and_ends, bookmarkStart_, bookmarkEnd_

# fixture components ---------------------------------------------

    @pytest.fixture
    def __all_starts_and_ends(self, request):
        return property_mock(
            request, _PartBookmarkFinder, '_all_starts_and_ends')

    @pytest.fixture
    def _add_to_names_so_far_(self, request):
        return method_mock(request,
                           _PartBookmarkFinder, '_add_to_names_so_far')

    @pytest.fixture
    def _all_starts_and_ends_(self, request):
        return method_mock(
            request, _PartBookmarkFinder, '_all_starts_and_ends')

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, _PartBookmarkFinder)

    @pytest.fixture
    def _iter_starts_(self, request):
        return method_mock(request, _PartBookmarkFinder, '_iter_starts')

    @pytest.fixture
    def _iter_start_end_pairs_(self, request):
        return method_mock(
            request, _PartBookmarkFinder, '_iter_start_end_pairs')

    @pytest.fixture
    def _matching_end_(self, request):
        return method_mock(request, _PartBookmarkFinder, '_matching_end')

    @pytest.fixture
    def _names_so_far_(self, request):
        return property_mock(request, _PartBookmarkFinder, '_names_so_far')

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, Part)
