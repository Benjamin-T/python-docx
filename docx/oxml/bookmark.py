# -*- coding: utf-8 -*-
"""
Custom element classes for bookmarks
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docx.oxml.simpletypes import ST_RelationshipId, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute


class CT_Bookmark(BaseOxmlElement):
    """The ``<w:bookmarkStart>`` element"""
    name = RequiredAttribute('w:name', ST_String)
    bmrk_id = RequiredAttribute('w:id', ST_RelationshipId)

class CT_MarkupRange(BaseOxmlElement):
    """The ``<w:bookmarkEnd>`` element."""
    bmrk_id = RequiredAttribute('w:id', ST_RelationshipId)


