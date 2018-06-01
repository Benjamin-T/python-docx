# -*- coding: utf-8 -*-
"""
Custom element classes for bookmarks
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docx.oxml.simpletypes import (ST_DecimalNumber, ST_RelationshipId,
                                   ST_String)
from docx.oxml.xmlchemy import (BaseOxmlElement, OptionalAttribute,
                                RequiredAttribute)


class CT_Bookmark(BaseOxmlElement):
    """The ``<w:bookmarkStart>`` element"""
    id = RequiredAttribute('w:id', ST_RelationshipId)
    name = RequiredAttribute('w:name', ST_String)


class CT_MarkupRange(BaseOxmlElement):
    """The ``<w:bookmarkEnd>`` element."""
    id = RequiredAttribute('w:id', ST_RelationshipId)
    colFirst = OptionalAttribute('w:colFirst', ST_DecimalNumber)
    colLast = OptionalAttribute('w:colLast', ST_DecimalNumber)
