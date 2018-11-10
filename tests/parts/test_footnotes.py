# encoding: utf-8

"""
Test suite for the docx.parts.footnotes module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.footnotes import FootnotesPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeFootnotesPart(object):

    def it_is_used_by_loader_to_construct_footnotes_part(
            self, request, package_, load_, footnotes_part_):
        partname, blob, content_type = 'partname', 'blob', CT.WML_FOOTNOTES
        load_.return_value = footnotes_part_

        part = PartFactory(partname, content_type, None, blob, package_)

        load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is footnotes_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def load_(self, request):
        return method_mock(request, FootnotesPart, 'load')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def footnotes_part_(self, request):
        return instance_mock(request, FootnotesPart)
