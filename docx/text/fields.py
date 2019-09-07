# encoding: utf-8

"""
Field-related proxy types.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.enum.fields import WD_FIELDCODE
from docx.oxml.simpletypes import ST_FldCharType
from docx.shared import ElementProxy
from docx.text.run import Run
from docx.oxml.shared import qn

class _SimpleField(object):
    def __init__(self, field, field_run):
        self._fieldText = field
        self._field_run = field_run

    @property
    def field_run(self):
        return self._field_run

    @property
    def field_text(self):
        return self._fieldText.instr


class _Field(object):
    def __init__(self, field, field_run, result_run):
        self._fieldText, self._fieldResult = field
        self._field_run = field_run
        self._result_run = result_run

    @property
    def field_run(self):
        return self._field_run

    @property
    def result_run(self):
        return self._result_run

    @property
    def field_text(self):
        return self._fieldText.text

    @property
    def result_text(self):
        return self._fieldResult.text

    @result_text.setter
    def result_text(self, text):
        self._fieldResult.text = text


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

        return _Field((fieldText, fieldResult), self._fld_run, self._fld_result)

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

