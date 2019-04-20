# encoding: utf-8

"""Step implementations for bookmark-related features."""

from __future__ import absolute_import, division, print_function, unicode_literals

from behave import given, then

from docx import Document

from helpers import test_docx


# given ===================================================


@given("a Bookmarks object of length 5 as bookmarks")
def given_a_Bookmarks_object_of_length_5_as_bookmarks(context):
    document = Document(test_docx("bmk-bookmarks"))
    context.bookmarks = document.bookmarks


# then =====================================================


@then("bookmark.id is an int")
def then_bookmark_id_is_an_int(context):
    bookmark = context.bookmark
    assert isinstance(bookmark.id, int)

@when("I remove bookmark {name} by {identifier}")
def when_I_remove_a_bookmark_named_bookmark_body(context, name, identifier):
    if identifier == 'index':
        name = int(name)
    del context.bookmarks[name]

@when("I get bookmarks[{idx}] as bookmark")
def when_I_get_bookmarks_3_as_bookmark(context, idx):
    context.bookmark = context.bookmarks[int(idx)]


# then =====================================================

@then('bookmark.name == "Target"')
def then_bookmark_name_eq_Target(context):
    bookmark = context.bookmark
    assert bookmark.name == "Target"


@then('bookmarks.get({name}) returns bookmark named "{name}" with id {id}')
def then_bookmark_get_returns_bookmark_object(context, name, id):
    bookmark = context.bookmarks.get(name)
    assert bookmark.name == name
    assert bookmark.id == int(id)


@then("bookmarks[{idx}] is a _Bookmark object")
def then_bookmarks_idx_is_a_Bookmark_object(context, idx):
    item = context.bookmarks[int(idx)]
    expected = "_Bookmark"
    actual = item.__class__.__name__
    assert actual == expected, "bookmarks[%s] is a %s object" % (idx, actual)


@then("iterating bookmarks produces {n} _Bookmark objects")
def then_iterating_bookmarks_produces_n_Bookmark_objects(context, n):
    items = [item for item in context.bookmarks]
    assert len(items) == int(n)
    assert all(item.__class__.__name__ == "_Bookmark" for item in items)


@then("len(bookmarks) == {count}")
def then_len_bookmarks_eq_count(context, count):
    expected = int(count)
    actual = len(context.bookmarks)
    assert actual == expected, "len(bookmarks) == %s" % actual


@then("no bookmark named {name} is found in document")
def then_no_bookmark_named_bookmark_body_is_found_in_document(context, name):
    context.exception = None
    try:
        context.bookmarks.get(name=name)
    except KeyError as exception:
        context.exception = exception
    assert context.exception.args == ("Requested bookmark not found.",)


@then("bookmark.empty == {bool_val}")
def bookmarks_empty_is_true(context, bool_val):
    assert context.bookmark.empty == eval(bool_val)
