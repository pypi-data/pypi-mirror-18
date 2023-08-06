# -*- coding: utf-8 -*-
u"""
This module implements LaTeX base classes that can be subclassed.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import with_statement
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import super
from builtins import open
from future import standard_library
standard_library.install_aliases()
from collections import UserList
from ordered_set import OrderedSet
from pylatex.utils import dumps_list
from contextlib import contextmanager
from io import open


class BaseLaTeXClass(object):

    u"""A class that has some basic functions for LaTeX functions.

    :param packages: :class:`pylatex.package.Package` instances

    :type packages: list

    """

    def __init__(self, packages=None):

        if packages is None:
            packages = []

        self.packages = OrderedSet(packages)

    def dumps(self):
        u"""Represent the class as a string in LaTeX syntax.

        This method should be implemented by any class that subclasses this
        class.
        """

    def dump(self, file_):
        u"""Write the LaTeX representation of the class to a file.

        :param file_: The file object in which to save the data

        :type file_: io.TextIOBase
        """

        file_.write(self.dumps())

    def generate_tex(self, filepath):
        u"""Generate a .tex file.

        :param filepath: the name of the file (without .tex)
        :type filepath: str
        """

        with open(filepath + u'.tex', u'w', encoding=u'utf-8') as newf:
            self.dump(newf)

    def dumps_packages(self):
        u"""Represent the packages needed as a string in LaTeX syntax.

        :return:
        :rtype: list
        """

        return dumps_list(self.packages)

    def dump_packages(self, file_):
        u"""Write the LaTeX representation of the packages to a file.

        :param file_: The file object in which to save the data

        :type file_: io.TextIOBase
        """

        file_.write(self.dumps_packages())


class BaseLaTeXContainer(BaseLaTeXClass, UserList):

    u"""A base class that can cointain other LaTeX content.

    :param data:
    :param packages: :class:`pylatex.package.Package` instances

    :type data: list
    :type packages: list
    """

    # TODO: Find a way to document multiple types, in this case str as well

    def __init__(self, data=None, packages=None):

        if data is None:
            data = []
        elif not isinstance(data, list):
            # If the data is not already a list make it a list, otherwise list
            # operations will not work
            data = [data]

        self.data = data
        self.real_data = data  # Always the data of this instance

        super(BaseLaTeXContainer, self).__init__(packages=packages)

    def dumps(self, **kwargs):
        u"""Represent the container as a string in LaTeX syntax.

        :return:
        :rtype: list
        """

        self.propegate_packages()

        return dumps_list(self, **kwargs)

    def propegate_packages(self):
        u"""Make sure packages get propegated."""

        for item in self.data:
            if isinstance(item, BaseLaTeXClass):
                if isinstance(item, BaseLaTeXContainer):
                    item.propegate_packages()
                for p in item.packages:
                    self.packages.add(p)

    def dumps_packages(self):
        u"""Represent the packages needed as a string in LaTeX syntax.

        :return:
        :rtype: list
        """

        self.propegate_packages()

        return dumps_list(self.packages)

    @contextmanager
    def create(self, child):
        u"""Add a LaTeX object to current container, context-manager style.

        :param child: An object to be added to the current container
        """

        prev_data = self.data
        self.data = child.data  # This way append works appends to the child

        yield child  # allows with ... as to be used as well

        self.data = prev_data
        self.append(child)


class BaseLaTeXNamedContainer(BaseLaTeXContainer):

    u"""A base class for containers with a basic begin end syntax.

    :param name:
    :param options:
    :param argument:

    :type name: str
    :type options: str or list or :class:`pylatex.parameters.Options` instance
    :type argument: str
    """

    def __init__(self, options=None, argument=None,
                 seperate_paragraph=False, begin_paragraph=False,
                 end_paragraph=False, **kwargs):
        if not hasattr(self, u'container_name'):
            self.container_name = self.__class__.__name__.lower()

        self.options = options
        self.argument = argument
        self.seperate_paragraph = seperate_paragraph
        self.begin_paragraph = begin_paragraph
        self.end_paragraph = end_paragraph

        super(BaseLaTeXNamedContainer, self).__init__(**kwargs)

    def dumps(self):
        u"""Represent the named container as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        string = u''

        if self.seperate_paragraph or self.begin_paragraph:
            string += u'\n\n'

        string += ur'\begin{' + self.container_name + u'}'

        if self.options is not None:
            string += u'[' + self.options + u']'

        if self.argument is not None:
            string += u'{' + self.argument + u'}'

        string += u'\n'

        string += super(BaseLaTeXNamedContainer, self).dumps()

        string += u'\n' + ur'\end{' + self.container_name + u'}'

        if self.seperate_paragraph or self.end_paragraph:
            string += u'\n\n'

        return string
