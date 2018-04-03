# encoding: utf-8

"""
Step implementations for bookmark-related features
"""

from behave import given, then, when

from docx import Document
from helpers import test_docx
from docx.text.bookmarks import Bookmark, Bookmarks

# given ===================================================


# when ====================================================

@when('I start a body bookmark')
def when_I_start_a_body_bookmark(context):
    bmrk = context.document.start_bookmark(name="test_bookmark")
    context.bmrk = bmrk

@when('I start a paragraph bookmark')
def when_I_start_a_paragraph_bookmark(context):
    par = context.document.add_paragraph()
    bmrk = par.start_bookmark(name="test_bookmark")
    context.bmrk = bmrk

@when('I start a run bookmark')
def when_I_start_a_run_bookmark(context):
    bmrk = context.run.start_bookmark(name="test_bookmark")
    context.bmrk = bmrk

@when('I end a bookmark')
def when_I_end_a_bookmark(context):
    context.document.end_bookmark(context.bmrk)

# then =====================================================

@then('the document contains a bookmark')
def then_the_document_contains_a_bookmark(context):
    bookmarks = context.document.bookmarks
    bookmark = bookmarks[-1]
    assert isinstance(bookmark, Bookmark)
