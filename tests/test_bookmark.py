# encoding: utf-8

"""Test suite for the docx.bookmark module."""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.bookmark import (
    _Bookmark,
    BookmarkParent,
    Bookmarks,
    _DocumentBookmarkFinder,
    _PartBookmarkFinder,
)
from docx.opc.part import Part, XmlPart
from docx.parts.document import DocumentPart

from .unitutil.cxml import element, xml
from .unitutil.mock import (
    ANY,
    call,
    class_mock,
    initializer_mock,
    instance_mock,
    method_mock,
    property_mock,
)


class DescribeBookmark(object):
    def it_has_name_property(self):
        bookmarkStart = element("w:bookmarkStart{w:name=bmk-0}")
        bookmarkEnd = element("w:bookmarkEnd")

        bookmark = _Bookmark((bookmarkStart, bookmarkEnd))

        assert bookmark.name == "bmk-0"

    def it_has_an_id_property(self):
        bookmarkStart = element("w:bookmarkStart{w:id=0}")
        bookmarkEnd = element("w:bookmarkEnd")

        bookmark = _Bookmark((bookmarkStart, bookmarkEnd))

        assert bookmark.id == 0

    def it_knows_its_empty(self, empty_fixture):
        bookmarkStart, bookmarkEnd, expected = empty_fixture

        bookmark = _Bookmark((bookmarkStart, bookmarkEnd))

        assert bookmark.empty == expected

    @pytest.fixture(
        params=[
            ("w:p/(w:bookmarkStart,w:bookmarkEnd)", True),
            ("w:p/(w:bookmarkStart,w:r,w:bookmarkEnd)", False),
            ("w:p/(w:bookmarkStart)", False),
        ]
    )
    def empty_fixture(self, request):
        cxml, expected = request.param
        paragraph = element(cxml)
        bookmarkStart = paragraph.getchildren()[0]
        bookmarkEnd = paragraph.getchildren()[-1]
        if bookmarkStart == bookmarkEnd:
            bookmarkEnd = None
        return bookmarkStart, bookmarkEnd, expected


class DescribeBookmarkParent(object):
    def it_can_add_a_bookmark_to_different_elements(self, start_bookmark_fixture):
        DocumentPart_, next_id_, element_, expected_xml = start_bookmark_fixture

        parent = BookmarkParent()
        parent.part = DocumentPart_
        parent._element = element_
        bookmark = parent.start_bookmark("bmk-1")

        assert parent._element.xml == expected_xml
        assert bookmark.name == "bmk-1"
        assert bookmark.id == 0
        assert bookmark._bookmarkEnd is None
        next_id_.assert_called_once_with()

    def it_can_close_an_open_bookmark(self, end_bookmark_fixture):
        element_, expected_xml = end_bookmark_fixture
        parent = BookmarkParent()

        parent._element = element_

        bookmarkStart = parent._element.xpath(".//w:bookmarkStart")[0]
        bmk = _Bookmark((bookmarkStart, None))

        bookmark = parent.end_bookmark(bmk)

        assert bookmark.id == 0
        assert bookmark.name == "bmk-1"
        assert bookmark._bookmarkEnd.id == 0
        assert parent._element.xml == expected_xml

    def it_raises_a_key_error_if_bookmark_name_already_in_document(
        self, DocumentPart_, next_id_, bookmark_names_
    ):
        parent = BookmarkParent()
        parent.part = DocumentPart_
        next_id_.return_value = 1
        parent._element = element("w:body")
        bookmark_names_.return_value = ["bmk-0", "bmk-2"]

        with pytest.raises(KeyError) as exc:
            parent.start_bookmark("bmk-0")
        assert "Bookmark name already present in document." in str(exc.value)

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (
                "w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0})",
                "w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}, w:bookmarkEnd{w:id=0})",
            ),
            (
                "w:body/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p)",
                "w:body/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p, w:bookmarkEnd{w:id=0})",
            ),
            (
                "w:ftr/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p)",
                "w:ftr/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p, w:bookmarkEnd{w:id=0})",
            ),
            (
                "w:hdr/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p)",
                "w:hdr/(w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0}), w:p, w:bookmarkEnd{w:id=0})",
            ),
        ]
    )
    def end_bookmark_fixture(self, request):
        cxml, expected_cxml = request.param
        parent = element(cxml)
        expected_xml = xml(expected_cxml)
        return parent, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", "w:p/(w:bookmarkStart{w:name=bmk-1, w:id=0})"),
            ("w:body", "w:body/(w:bookmarkStart{w:name=bmk-1, w:id=0})"),
            ("w:ftr", "w:ftr/(w:bookmarkStart{w:name=bmk-1, w:id=0})"),
            ("w:hdr", "w:hdr/(w:bookmarkStart{w:name=bmk-1, w:id=0})"),
        ]
    )
    def start_bookmark_fixture(self, request, DocumentPart_, next_id_, bookmark_names_):
        cxml, expected_cxml = request.param
        expected_xml = xml(expected_cxml)
        element_ = element(cxml)
        next_id_.return_value = 0
        bookmark_names_.return_value = ["bmk-0", "bmk-2"]

        return DocumentPart_, next_id_, element_, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Bookmarks_(self, request):
        return instance_mock(request, Bookmarks)

    @pytest.fixture
    def DocumentPart_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _DocumentBookmarkFinder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def bookmark_names_(self, request):
        return property_mock(request, _DocumentBookmarkFinder, "bookmark_names")

    @pytest.fixture
    def next_id_(self, request):
        return property_mock(request, _DocumentBookmarkFinder, "next_id")


class DescribeBookmarks(object):
    def it_can_delete_a_bookmark_by_index(self, del_by_index_fixture):
        bookmarks, parent, bookmarks__getitem__, expected_xml = del_by_index_fixture

        del bookmarks[0]

        assert parent.xml == expected_xml
        bookmarks__getitem__.assert_called_once_with(bookmarks, 0)

    def it_can_delete_a_bookmark_by_name(self, del_by_name_fixture):
        bookmarks, parent, get_, expected_xml = del_by_name_fixture

        del bookmarks["bmk-1"]

        assert parent.xml == expected_xml
        get_.assert_called_once_with(bookmarks, "bmk-1")

    def it_provides_access_to_bookmarks_by_index(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(3))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(3))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        bookmark = bookmarks[1]

        _Bookmark_.assert_called_once_with((bookmarkStarts[1], bookmarkEnds[1]))
        assert bookmark == bookmark_

    def it_provides_access_to_bookmarks_by_name(self, bookmark_by_name_fixture):
        bookmarks, names = bookmark_by_name_fixture

        for name in names:
            bmrk = bookmarks.get(name=name)
            assert bmrk.name == name

        with pytest.raises(Exception) as exc:
            bookmarks.get(name="foo-bar")
            assert exc == KeyError("Requested bookmark not found.")

    def it_provides_access_to_bookmarks_by_slice(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(4))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(4))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        bookmarks_slice = bookmarks[1:3]

        assert _Bookmark_.call_args_list == [
            call((bookmarkStarts[1], bookmarkEnds[1])),
            call((bookmarkStarts[2], bookmarkEnds[2])),
        ]
        assert bookmarks_slice == [bookmark_, bookmark_]

    def it_can_iterate_its_bookmarks(
        self, _finder_prop_, finder_, _Bookmark_, bookmark_
    ):
        bookmarkStarts = tuple(element("w:bookmarkStart") for _ in range(3))
        bookmarkEnds = tuple(element("w:bookmarkEnd") for _ in range(3))
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = list(zip(bookmarkStarts, bookmarkEnds))
        _Bookmark_.return_value = bookmark_
        bookmarks = Bookmarks(None)

        _bookmarks = list(b for b in bookmarks)

        assert _Bookmark_.call_args_list == [
            call((bookmarkStarts[0], bookmarkEnds[0])),
            call((bookmarkStarts[1], bookmarkEnds[1])),
            call((bookmarkStarts[2], bookmarkEnds[2])),
        ]
        assert _bookmarks == [bookmark_, bookmark_, bookmark_]

    def it_knows_how_many_bookmarks_the_document_contains(self, _finder_prop_, finder_):
        _finder_prop_.return_value = finder_
        finder_.bookmark_pairs = tuple((1, 2) for _ in range(42))
        bookmarks = Bookmarks(None)

        count = len(bookmarks)

        assert count == 42

    def it_provides_access_to_its_bookmark_finder_to_help(
        self, document_part_, _DocumentBookmarkFinder_, finder_
    ):
        _DocumentBookmarkFinder_.return_value = finder_
        bookmarks = Bookmarks(document_part_)

        finder = bookmarks._finder

        _DocumentBookmarkFinder_.assert_called_once_with(document_part_)
        assert finder is finder_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def bookmark_by_name_fixture(self, request, bookmarks__iter__):
        bookmarks = Bookmarks(None)
        names = ["test-0", "test-1", "test-12"]

        bookmark_lst = [instance_mock(request, _Bookmark) for _ in range(3)]
        for bmrk, name in zip(bookmark_lst, names):
            bmrk.name = name

        bookmarks__iter__.return_value = iter(bookmark_lst)

        return bookmarks, names

    @pytest.fixture(
        params=[
            ("w:p/(w:bookmarkStart,w:bookmarkEnd)", "w:p"),
            ("w:body/(w:p/(w:bookmarkStart), w:p/(w:bookmarkEnd))", "w:body/(w:p,w:p)"),
            (
                "w:body/(w:p/(w:bookmarkStart, w:bookmarkStart), w:p/(w:bookmarkEnd))",
                "w:body/(w:p/(w:bookmarkStart), w:p)",
            ),
        ]
    )
    def del_by_index_fixture(self, request, bookmarks__getitem__):
        cxml, expected_cxml = request.param
        parent = element(cxml)
        expected_xml = xml(expected_cxml)

        bookmarkStart = parent.xpath(".//w:bookmarkStart")[0]
        bookmarkEnd = parent.xpath(".//w:bookmarkEnd")[0]
        bookmark_ = _Bookmark((bookmarkStart, bookmarkEnd))

        bookmarks = Bookmarks(None)
        bookmarks__getitem__.return_value = bookmark_

        return bookmarks, parent, bookmarks__getitem__, expected_xml

    @pytest.fixture(
        params=[
            ("w:p/(w:bookmarkStart,w:bookmarkEnd)", "w:p"),
            ("w:body/(w:p/(w:bookmarkStart), w:p/(w:bookmarkEnd))", "w:body/(w:p,w:p)"),
            (
                "w:body/(w:p/(w:bookmarkStart, w:bookmarkStart), w:p/(w:bookmarkEnd))",
                "w:body/(w:p/(w:bookmarkStart), w:p)",
            ),
        ]
    )
    def del_by_name_fixture(self, request, get_):
        cxml, expected_cxml = request.param
        parent = element(cxml)
        expected_xml = xml(expected_cxml)

        bookmarkStart = parent.xpath(".//w:bookmarkStart")[0]
        bookmarkEnd = parent.xpath(".//w:bookmarkEnd")[0]
        bookmark_ = _Bookmark((bookmarkStart, bookmarkEnd))

        bookmarks = Bookmarks(None)
        get_.return_value = bookmark_

        return bookmarks, parent, get_, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Bookmark_(self, request):
        return class_mock(request, "docx.bookmark._Bookmark")

    @pytest.fixture
    def bookmark_(self, request):
        return instance_mock(request, _Bookmark)

    @pytest.fixture
    def bookmarks__getitem__(self, request):
        return method_mock(request, Bookmarks, "__getitem__")

    @pytest.fixture
    def bookmarks__iter__(self, request):
        return method_mock(request, Bookmarks, "__iter__")

    @pytest.fixture
    def _DocumentBookmarkFinder_(self, request):
        return class_mock(request, "docx.bookmark._DocumentBookmarkFinder")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def finder_(self, request):
        return instance_mock(request, _DocumentBookmarkFinder)

    @pytest.fixture
    def _finder_prop_(self, request):
        return property_mock(request, Bookmarks, "_finder")

    @pytest.fixture
    def get_(self, request):
        return method_mock(request, Bookmarks, "get")


class Describe_DocumentBookmarkFinder(object):
    def it_finds_all_the_bookmark_pairs_in_the_document(
        self, pairs_fixture, _PartBookmarkFinder_
    ):
        document_part_, calls, expected_value = pairs_fixture
        document_bookmark_finder = _DocumentBookmarkFinder(document_part_)

        bookmark_pairs = document_bookmark_finder.bookmark_pairs

        document_part_.iter_story_parts.assert_called_once_with()
        assert _PartBookmarkFinder_.iter_start_end_pairs.call_args_list == calls
        assert bookmark_pairs == expected_value

    def it_provides_access_to_the_bookmark_names(self, bookmark_starts_):
        document_bookmark_finder = _DocumentBookmarkFinder(None)

        bmk_starts = (
            (0, _Bookmark((element("w:bookmarkStart{w:name=bmk-1}"), None))),
            (1, _Bookmark((element("w:bookmarkStart{w:name=bmk-2}"), None))),
        )
        bookmark_starts_.return_value = bmk_starts

        names = document_bookmark_finder.bookmark_names

        assert names == ["bmk-1", "bmk-2"]

    def it_finds_all_the_bookmark_starts_in_the_document(
        self, starts_fixture, _PartBookmarkFinder_
    ):
        document_part_, calls, expected_value = starts_fixture
        document_bookmark_finder = _DocumentBookmarkFinder(document_part_)

        bookmark_starts = document_bookmark_finder.bookmark_starts

        document_part_.iter_story_parts.assert_called_once_with()
        assert _PartBookmarkFinder_.iter_starts.call_args_list == calls
        assert bookmark_starts == expected_value

    def it_provides_the_lowest_available_id_to_help(self, next_id_fixture):
        bookmark_starts_, expected_id = next_id_fixture
        bookmarks = _DocumentBookmarkFinder(None)

        next_id = bookmarks.next_id

        bookmark_starts_.assert_called_once_with()
        assert next_id == expected_id

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[(0, 1, 2), (0, 3, 1), (0, 42, 1)])
    def next_id_fixture(self, request, bookmark_starts_):
        id_1, id_2, expected_id = request.param

        bmk_starts = (
            (0, _Bookmark((element("w:bookmarkStart{w:id=%d}" % id_1), None))),
            (1, _Bookmark((element("w:bookmarkStart{w:id=%d}" % id_2), None))),
        )

        bookmark_starts_.return_value = bmk_starts
        return bookmark_starts_, expected_id

    @pytest.fixture(
        params=[
            ([[(1, 2)]], [(1, 2)]),
            ([[(1, 2), (3, 4), (5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            ([[(1, 2)], [(3, 4)], [(5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            (
                [[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]],
                [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)],
            ),
        ]
    )
    def pairs_fixture(self, request, document_part_, _PartBookmarkFinder_):
        parts_pairs, expected_value = request.param
        mock_parts = [
            instance_mock(request, Part, name="Part-%d" % idx)
            for idx, part_pairs in enumerate(parts_pairs)
        ]
        calls = [call(part_) for part_ in mock_parts]

        document_part_.iter_story_parts.return_value = (p for p in mock_parts)
        _PartBookmarkFinder_.iter_start_end_pairs.side_effect = parts_pairs

        return document_part_, calls, expected_value

    @pytest.fixture(
        params=[
            ([[(1, 2)]], [(1, 2)]),
            ([[(1, 2), (3, 4), (5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            ([[(1, 2)], [(3, 4)], [(5, 6)]], [(1, 2), (3, 4), (5, 6)]),
            (
                [[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]],
                [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)],
            ),
        ]
    )
    def starts_fixture(self, request, document_part_, _PartBookmarkFinder_):
        parts_pairs, expected_value = request.param
        mock_parts = [
            instance_mock(request, Part, name="Part-%d" % idx)
            for idx, part_pairs in enumerate(parts_pairs)
        ]
        calls = [call(part_) for part_ in mock_parts]

        document_part_.iter_story_parts.return_value = (p for p in mock_parts)
        _PartBookmarkFinder_.iter_starts.side_effect = parts_pairs

        return document_part_, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def bookmark_starts_(self, request):
        return property_mock(request, _DocumentBookmarkFinder, "bookmark_starts")

    @pytest.fixture
    def _PartBookmarkFinder_(self, request):
        return class_mock(request, "docx.bookmark._PartBookmarkFinder")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)


class Describe_PartBookmarkFinder(object):
    """Unit tests for _PartBookmarkFinder class"""

    def it_provides_an_iter_start_end_pairs_interface_method(
        self, part_, _init_, _iter_start_end_pairs_
    ):
        pairs = _PartBookmarkFinder.iter_start_end_pairs(part_)

        _init_.assert_called_once_with(ANY, part_)
        _iter_start_end_pairs_.assert_called_once_with(ANY)
        assert pairs == _iter_start_end_pairs_.return_value

    def it_gathers_all_the_bookmark_start_and_end_elements_to_help(self, part_):
        body = element("w:body/(w:bookmarkStart,w:p,w:bookmarkEnd,w:p,w:bookmarkStart)")
        part_.element = body
        finder = _PartBookmarkFinder(part_)

        starts_and_ends = finder._all_starts_and_ends

        assert starts_and_ends == [body[0], body[2], body[4]]

    def it_iterates_start_end_pairs_to_help(
        self, _iter_starts_, _matching_end_, _name_already_used_
    ):
        bookmarkStarts = tuple(
            element("w:bookmarkStart{w:name=%s,w:id=%d}" % (name, idx))
            for idx, name in enumerate(("bmk-0", "bmk-1", "bmk-2", "bmk-1"))
        )
        bookmarkEnds = (
            None,
            element("w:bookmarkEnd{w:id=1}"),
            element("w:bookmarkEnd{w:id=2}"),
        )
        _iter_starts_.return_value = iter(enumerate(bookmarkStarts))
        _matching_end_.side_effect = (
            None,
            bookmarkEnds[1],
            bookmarkEnds[2],
            bookmarkEnds[1],
        )
        _name_already_used_.side_effect = (False, False, True)
        finder = _PartBookmarkFinder(None)

        start_end_pairs = list(finder._iter_start_end_pairs())

        assert _matching_end_.call_args_list == [
            call(finder, bookmarkStarts[0], 0),
            call(finder, bookmarkStarts[1], 1),
            call(finder, bookmarkStarts[2], 2),
            call(finder, bookmarkStarts[3], 3),
        ]
        assert _name_already_used_.call_args_list == [
            call(finder, "bmk-1"),
            call(finder, "bmk-2"),
            call(finder, "bmk-1"),
        ]
        assert start_end_pairs == [
            (bookmarkStarts[1], bookmarkEnds[1]),
            (bookmarkStarts[2], bookmarkEnds[2]),
        ]

    def it_iterates_bookmarkStart_elements_to_help(self, _all_starts_and_ends_prop_):
        starts_and_ends = (
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
            element("w:bookmarkStart"),
            element("w:bookmarkEnd"),
        )
        _all_starts_and_ends_prop_.return_value = list(starts_and_ends)
        finder = _PartBookmarkFinder(None)

        starts = list(finder._iter_starts())

        assert starts == [
            (0, starts_and_ends[0]),
            (2, starts_and_ends[2]),
            (4, starts_and_ends[4]),
        ]

    def it_finds_the_matching_end_for_a_start_to_help(
        self, matching_end_fixture, _all_starts_and_ends_prop_
    ):
        starts_and_ends, start_idx, expected_value = matching_end_fixture
        _all_starts_and_ends_prop_.return_value = starts_and_ends
        bookmarkStart = starts_and_ends[start_idx]
        finder = _PartBookmarkFinder(None)

        bookmarkEnd = finder._matching_end(bookmarkStart, start_idx)

        assert bookmarkEnd == expected_value

    def it_knows_whether_a_bookmark_name_was_already_used(
        self, name_used_fixture, _names_so_far_prop_, names_so_far_
    ):
        name, is_used, calls, expected_value = name_used_fixture
        _names_so_far_prop_.return_value = names_so_far_
        names_so_far_.__contains__.return_value = is_used
        finder = _PartBookmarkFinder(None)

        already_used = finder._name_already_used(name)

        assert names_so_far_.add.call_args_list == calls
        assert already_used is expected_value

    def it_composes_a_set_in_which_to_track_used_bookmark_names(self):
        finder = _PartBookmarkFinder(None)
        names_so_far = finder._names_so_far
        assert names_so_far == set()

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            # ---no subsequent end---
            ([element("w:bookmarkStart{w:name=foo,w:id=0}")], 0, None),
            # ---no matching end---
            (
                [element("w:bookmarkStart{w:id=0}"), element("w:bookmarkEnd{w:id=1}")],
                0,
                None,
            ),
            # ---end immediately follows start---
            (
                [element("w:bookmarkStart{w:id=0}"), element("w:bookmarkEnd{w:id=0}")],
                0,
                1,
            ),
            # ---end separated from start by other start---
            (
                [
                    element("w:bookmarkStart{w:name=foo,w:id=0}"),
                    element("w:bookmarkStart{w:name=bar,w:id=0}"),
                    element("w:bookmarkEnd{w:id=0}"),
                ],
                0,
                2,
            ),
            # ---end separated from start by other end---
            (
                [
                    element("w:bookmarkStart{w:name=foo,w:id=1}"),
                    element("w:bookmarkEnd{w:id=0}"),
                    element("w:bookmarkEnd{w:id=1}"),
                ],
                0,
                2,
            ),
        ]
    )
    def matching_end_fixture(self, request):
        starts_and_ends, start_idx, end_idx = request.param
        expected_value = None if end_idx is None else starts_and_ends[end_idx]
        return starts_and_ends, start_idx, expected_value

    @pytest.fixture(params=[(True, True), (False, False)])
    def name_used_fixture(self, request):
        is_used, expected_value = request.param
        name = "George"
        calls = [] if is_used else [call("George")]
        return name, is_used, calls, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _all_starts_and_ends_prop_(self, request):
        return property_mock(request, _PartBookmarkFinder, "_all_starts_and_ends")

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, _PartBookmarkFinder)

    @pytest.fixture
    def _iter_start_end_pairs_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_iter_start_end_pairs")

    @pytest.fixture
    def _iter_starts_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_iter_starts")

    @pytest.fixture
    def _matching_end_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_matching_end")

    @pytest.fixture
    def _name_already_used_(self, request):
        return method_mock(request, _PartBookmarkFinder, "_name_already_used")

    @pytest.fixture
    def _names_so_far_prop_(self, request):
        return property_mock(request, _PartBookmarkFinder, "_names_so_far")

    @pytest.fixture
    def names_so_far_(self, request):
        return instance_mock(request, set)

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, XmlPart)
