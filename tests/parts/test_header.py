# encoding: utf-8

"""
Test suite for the docx.parts.header module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.header import HeaderPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeHeaderPart(object):

    def it_is_used_by_loader_to_construct_header_part(
            self, request, package_, load_, header_part_):
        partname, blob, content_type = 'partname', 'blob', CT.WML_HEADER
        load_.return_value = header_part_

        part = PartFactory(partname, content_type, None, blob, package_)

        load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is header_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def load_(self, request):
        return method_mock(request, HeaderPart, 'load')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)
