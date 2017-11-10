# -*- coding: utf-8 -*-
"""
Custom element classes for bookmarks
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docx.oxml.simpletypes import ST_RelationshipId, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute


class CT_BookmarkStart(BaseOxmlElement):
    """The ``<w:bookmarkStart>`` element"""
    name = RequiredAttribute('w:name', ST_String)
    bmrk_id = RequiredAttribute('w:id', ST_RelationshipId)

    @property
    def _next_id(self):
        """
        The `_next_id` property is used to get the next index based on
        the total amount of bookmarkStart elements already in the document
        """
        root = self.getroottree().getroot()
        return str(len(root.xpath('.//w:bookmarkStart')))

    @property
    def is_closed(self):
        """
        The `is_closed` property of the :class:`CT_BookmarkStart` object is
        used to determine whether there is already a bookmarkEnd element in
        the document containing the same bookmark id. If this is the case, the
        bookmark is closed if not, the bookmark is open.
        """
        root_element = self.getroottree().getroot()
        matching_bookmarkEnds = root_element.xpath(
            './/w:bookmarkEnd[@w:id=\'%s\']' % self.bmrk_id
        )
        if not matching_bookmarkEnds:
            return False
        return True


class CT_BookmarkEnd(BaseOxmlElement):
    """The ``<w:bookmarkEnd>`` element."""
    bmrk_id = RequiredAttribute('w:id', ST_RelationshipId)

    @property
    def _next_id(self):
        """
        The `_next_id` property is used to get the next index based on
        the total amount of bookmarkStart elements already in the document
        """
        root = self.getroottree().getroot()
        return str(len(root.xpath('.//w:bookmarkStart')))

    @property
    def is_closed(self):
        """
        The `is_closed` property is used to determine whether there is allready
        a bookmarkEnd element in the document containing the same bookmark id.
        """
        root_element = self.getroottree().getroot()
        matching_bookmarkEnds = root_element.xpath(
            './/w:bookmarkEnd[@w:id=\'%s\']' % self.bmrk_id
        )
        if len(matching_bookmarkEnds) == 1:
            return True
        return False
