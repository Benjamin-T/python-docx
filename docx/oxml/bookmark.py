# -*- coding: utf-8 -*-
"""
Custom element classes for bookmarks
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docx.oxml.simpletypes import ST_DecimalNumber, ST_String
from docx.oxml.xmlchemy import (BaseOxmlElement, OptionalAttribute,
                                RequiredAttribute)


class CT_Bookmark(BaseOxmlElement):
    """The ``<w:bookmarkStart>`` element"""
    id = RequiredAttribute('w:id', ST_DecimalNumber)
    name = RequiredAttribute('w:name', ST_String)

    def add_name(self, name):
        """
        Add the bookmark name to the `<w:bookmarkStart>` element.
        """
        self.id = self._next_id
        self.name = name

    @property
    def _next_id(self):
        """
        The first ``w:id`` unused by a ``<w:bookmarkStart>`` element, starting at
        1 and filling any gaps in numbering between existing ``<w:bookmarkStart>``
        elements.
        """
        root_element = [ancestor for ancestor in self.iterancestors()][-1]
        bmrk_id_strs = root_element.xpath('.//w:bookmarkStart/@w:id')
        bmrk_ids = [int(bmrk_id_str) for bmrk_id_str in bmrk_id_strs]
        for num in range(1, len(bmrk_ids)+2):
            if num not in bmrk_ids:
                break
        return num

    @property
    def is_closed(self):
        """
        The `is_closed` property of the :class:`CT_BookmarkRange` object is
        used to determine whether there is already a bookmarkEnd element in
        the document containing the same bookmark id. If this is the case, the
        bookmark is closed if not, the bookmark is open.
        """
        root_element = [ancestor for ancestor in self.iterancestors()][-1]
        matching_bookmarkEnds = root_element.xpath(
            './/w:bookmarkEnd[@w:id=\'%s\']' % self.id
        )
        if not matching_bookmarkEnds:
            return False
        return True


class CT_MarkupRange(BaseOxmlElement):
    """The ``<w:bookmarkEnd>`` element."""
    id = RequiredAttribute('w:id', ST_DecimalNumber)
    colFirst = OptionalAttribute('w:colFirst', ST_DecimalNumber)
    colLast = OptionalAttribute('w:colLast', ST_DecimalNumber)
