# -*- coding: utf-8 -*-
"""
Custom element classes for bookmarks
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docx.oxml.simpletypes import ST_RelationshipId, ST_String, ST_DecimalNumber
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute, OptionalAttribute

class CT_Bookmark(BaseOxmlElement):
    """The ``<w:bookmarkStart>`` element"""
    id = RequiredAttribute('w:id', ST_RelationshipId)
    name = RequiredAttribute('w:name', ST_String)

    def add_name(self, name):
        """
        Return a newly added CT_Num (<w:num>) element referencing the
        abstract numbering definition identified by *abstractNum_id*.
        """
        self.id = self._next_id
        self.name = name

    def get_root_element(self):
        """
        Finds the highest root_element.
        This is done to make sure the whole document is checked for 
        bookmark id's.
        """
        _parent = self.getparent()
        count = 0
        while _parent is not None:
            _parent = _parent.getparent()
            count += 1
            if count == 10 or _parent is None:
                break
            root_element = _parent
            next
        return root_element

    @property
    def _next_id(self):
        """
        The first ``w:id`` unused by a ``<w:bookmarkStart>`` element, starting at
        1 and filling any gaps in numbering between existing ``<w:bookmarkStart>``
        elements.
        """
        root_element = self.get_root_element()
        bmrk_id_strs = root_element.xpath('.//w:bookmarkStart/@w:id')
        bmrk_ids = [int(bmrk_id_str) for bmrk_id_str in bmrk_id_strs]
        for num in range(1, len(bmrk_ids)+2):
            if num not in bmrk_ids:
                break
        return str(num)

    @property
    def is_closed(self):
        """
        The `is_closed` property of the :class:`CT_BookmarkRange` object is
        used to determine whether there is already a bookmarkEnd element in
        the document containing the same bookmark id. If this is the case, the
        bookmark is closed if not, the bookmark is open.
        """
        root_element = self.get_root_element()
        matching_bookmarkEnds = root_element.xpath(
            './/w:bookmarkEnd[@w:id=\'%s\']' % self.id
        )
        if not matching_bookmarkEnds:
            return False
        return True

class CT_MarkupRange(BaseOxmlElement):
    """The ``<w:bookmarkEnd>`` element."""
    id = RequiredAttribute('w:id', ST_RelationshipId)
    
    def get_root_element(self):
        """
        Finds the highest root_element.
        This is done to make sure the whole document is checked for 
        bookmark id's.

        """
        _parent = self.getparent()
        count = 0
        while _parent is not None:
            _parent = _parent.getparent()
            count += 1
            if count == 10 or _parent is None:
                break
            root_element = _parent
            next
        return root_element

    @property
    def is_closed(self):
        """
        The `is_closed` property of the :class:`CT_BookmarkRange` object is
        used to determine whether there is already a bookmarkEnd element in
        the document containing the same bookmark id. If this is the case, the
        bookmark is closed if not, the bookmark is open.
        """
        root_element = self.get_root_element()
        matching_bookmarkEnds = root_element.xpath(
            './/w:bookmarkEnd[@w:id=\'%s\']' % self.id
        )
        if not matching_bookmarkEnds:
            return False
        return True



