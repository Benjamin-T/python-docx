# encoding: utf-8

"""
Test suite for the docx.parts.endnotes module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.endnotes import EndnotesPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeEndnotesPart(object):

    def it_is_used_by_loader_to_construct_endnotes_part(
            self, request, package_, load_, endnotes_part_):
        partname, blob, content_type = 'partname', 'blob', CT.WML_ENDNOTES
        load_.return_value = endnotes_part_

        part = PartFactory(partname, content_type, None, blob, package_)

        load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is endnotes_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def load_(self, request):
        return method_mock(request, EndnotesPart, 'load')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def endnotes_part_(self, request):
        return instance_mock(request, EndnotesPart)
