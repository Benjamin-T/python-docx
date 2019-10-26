# encoding: utf-8

"""
Field-related proxy types.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain

from docx.compat import Sequence
from docx.enum.fields import WD_FIELDCODE
from docx.oxml.ns import qn
from docx.oxml.shared import qn
from docx.oxml.simpletypes import ST_FldCharType
from docx.shared import ElementProxy, lazyproperty
from docx.text.run import Run
from collections import deque


class Fields(Sequence):
    """Sequence of |Bookmark| objects.

    This object has mixed semantics. As a sequence, it supports indexed access
    (including slices), `len()`, and iteration (which will perform significantly
    better than repeated indexed access). It also supports some `dict` semantics on
    bookmark name. Specifically, the `in` operator can be used to detect the presence of
    a bookmark by name (e.g. `if name in bookmarks`) and it has a `get()` method that
    allows a bookmark to be retrieved by name.
    """

    def __init__(self, document_part):
        self._document_part = document_part

    def __getitem__(self, idx):
        """Supports indexed and sliced access."""
        fields = self._finder.fields
        if isinstance(idx, slice):
            return [field for field in fields[idx]]
        return fields[idx]

    def __iter__(self):
        """Supports iteration."""
        return (field for field in self._finder.fields)

    def __len__(self):
        return len(self._finder.fields)

    @lazyproperty
    def _finder(self):
        """_DocumentFieldFinder instance for this document."""
        return _DocumentFieldFinder(self._document_part)


class _SimpleField(object):
    def __init__(self, field):
        self._field_run = field

    @property
    def field_run(self):
        return self._field_run

    @property
    def field_text(self):
        str_lst = self._field_run.fldsimple_lst
        if len(str_lst):
            return str_lst[0].instr


class _Field(object):
    def __init__(self, field_runs):
        self._field_run, self._result_run = field_runs

    @property
    def field_run(self):
        return self._field_run

    @property
    def result_run(self):
        return self._result_run

    @property
    def field_text(self):
        str_lst = self._field_run.instrText_lst
        if str_lst:
            return str_lst[0].text

    @property
    def result_text(self):
        str_lst = self._result_run.instrText_lst
        if str_lst:
            return str_lst[0].text

    @result_text.setter
    def result_text(self, value):

        str_lst = self._result_run._r.instrText_lst
        if str_lst:
            str_lst[0].text = value


class ComplexField(ElementProxy):
    """
    """

    def __init__(self, field, parent):
        super(ComplexField, self).__init__(field, parent)
        self._fld_begin, self._fld_run, self._fld_seperate, self._fld_result, self._fld_end = (
            field
        )
        self._parent = parent

    @classmethod
    def new(cls, paragraph):
        _fldChars = []
        for fldCharType in ["begin", "fld_run", "separate", "fld_result", "end"]:
            run = paragraph.add_run()
            if fldCharType in ["begin", "separate", "end"]:
                run._r.add_fldChar(fldCharType)
            _fldChars.append(run)
        return cls(_fldChars, paragraph)

    # def _add_fldChar(self, fldChar):

    # @property
    # def fields(self):
    #     return [Field_(r, self._parent) for r in self._element.xpath('//w:r[w:fldChar]')]

    def add_field(self, field_name, properties="", prelim_value=None):
        # field_ = {
        #     WD_FIELDCODE.REF: "REF",
        #     WD_FIELDCODE.SEQ: "SEQ",
        #     WD_FIELDCODE.DATE: "DATE",
        #     WD_FIELDCODE.AUTHOR: "AUTHOR",
        # }[field_name]
        field_ = field_name._member_name

        fieldText = self._fld_run._r.add_instrText(field_)
        fieldText.text += " " + properties.strip()

        fieldResult = self._fld_result._r.add_instrText()
        if prelim_value is not None:
            fieldResult.text = prelim_value
        return _Field((self._fld_run, self._fld_result))

    # def insert_seperator(self):
    #     self.begin
    #     self._field_begin._add_fldChar()

    #     run = self._parent.add_run()
    #     fldChar = run._element._add_fldChar()
    #     fldChar.fldCharType = "separate"

    # def end_field(self):
    #     run = self._parent.add_run()
    #     fldChar = run._element._add_fldChar()
    #     fldChar.fldCharType = "end"
    #     return fldChar

    # @property
    # def begin(self):
    #     return Field_(*self._field_begin)
    #     #self._element.xpath('//w:fldChar[@w:fldCharType="begin"]')[0]

    # @property
    # def end(self):
    #     return Field_(*self._field_end)
    # return self._element.xpath('w:fldChar[@w:fldCharType="end"]')[0]


class _DocumentFieldFinder(object):
    def __init__(self, document_part):
        self._document_part = document_part

    @property
    def fields(self):
        """List of 'Simple' and 'Complex' fields in the document."""
        return list(
            chain(
                *(
                    _PartFieldFinder.iter_fields(part)
                    for part in self._document_part.iter_story_parts()
                )
            )
        )


class _PartFieldFinder(object):
    def __init__(self, part):
        self._part = part

    @classmethod
    def iter_fields(cls, part):
        """Generate each (bookmarkStart, bookmarkEnd) in *part*."""
        return cls(part)._iter_fields()

    def _iter_fields(self):
        return chain(self._simplefields(), self._complexfields())

    def _simplefields(self):
        return (
            _SimpleField(fld) for fld in self._part.element.xpath("//w:r[w:fldSimple]")
        )

    def _complexfields(self):
        for start_r, sep_r, _ in self._fieldchar_elements():
            field_run, result_run = start_r.getnext(), sep_r.getnext()
            yield _Field((field_run, result_run))

    def _fieldchar_elements(self):
        order = deque(maxlen=3)
        fld_chars = deque(maxlen=3)
        run_objs = deque(maxlen=3)
        for run in self._part.element.xpath("//w:r[w:fldChar]"):
            fld = run.fldChar_lst[0]
            order.append(fld.fldCharType)
            run_objs.append(run)
            fld_chars.append(fld)
            if order == deque(["begin", "separate", "end"]):
                yield run_objs
