# encoding: utf-8

"""|CommentsPart| and closely related objects"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.opc.part import XmlPart


class CommentsPart(XmlPart):
    """Package part containing comments."""
