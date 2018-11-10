# encoding: utf-8

"""
Test suite for the docx.parts.comments module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.comments import CommentsPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeCommentsPart(object):

    def it_is_used_by_loader_to_construct_comments_part(
            self, request, package_, load_, comments_part_):
        partname, blob, content_type = 'partname', 'blob', CT.WML_COMMENTS
        load_.return_value = comments_part_

        part = PartFactory(partname, content_type, None, blob, package_)

        load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is comments_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def load_(self, request):
        return method_mock(request, CommentsPart, 'load')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def comments_part_(self, request):
        return instance_mock(request, CommentsPart)
