# -*- coding: utf-8 -*-
u"""
This module implements the class that deals with sections.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import super
from future import standard_library
standard_library.install_aliases()
from . import Container, Command
from ..utils import dumps_list


class SectionBase(Container):

    u"""A class that is the base for all section type classes.

    :param title:
    :param numbering:
    :param data:

    :type title: str
    :type numbering: bool
    :type data: list
    """

    def __init__(self, title, numbering=True, data=None):
        self.title = title
        self.numbering = numbering

        super(SectionBase, self).__init__(data)

    def dumps(self):
        u"""Represent the section as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        if not self.numbering:
            num = u'*'
        else:
            num = u''

        section_type = self.__class__.__name__.lower()
        string = Command(section_type + num, self.title).dumps()
        string += dumps_list(self)

        super(SectionBase, self).dumps()

        return string
