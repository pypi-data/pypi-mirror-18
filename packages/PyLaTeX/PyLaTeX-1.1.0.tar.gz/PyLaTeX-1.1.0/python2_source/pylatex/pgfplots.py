# -*- coding: utf-8 -*-
u"""
This module implements the classes used to show plots.

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
from pylatex.base_classes import LatexObject, Environment, Command
from pylatex.package import Package


class TikZ(Environment):

    u"""Basic TikZ container class.

    :param data:

    :type data: list
    """

    container_name = u'tikzpicture'

    def __init__(self, data=None):

        packages = [Package(u'tikz')]

        super(TikZ, self).__init__(data=data, packages=packages)


class Axis(Environment):

    u"""PGFPlots axis container class, this contains plots.

    :param data:
    :param options:

    :type data: list
    :type options: str
    """

    def __init__(self, data=None, options=None):
        packages = [Package(u'pgfplots'), Command(u'pgfplotsset',
                                                 u'compat=newest')]

        super(Axis, self).__init__(data=data, options=options, packages=packages)


class Plot(LatexObject):

    ur"""A class representing a PGFPlot.

    :param name:
    :param func:
    :param coordinates:
    :param options:

    :type name: str
    :type func: str
    :type coordinates: list
    :type options: str

    TODO:

    options type can also be list or
        :class:`~pylatex.base_classes.command.Options` instance
    """

    def __init__(self, name=None, func=None, coordinates=None, options=None):
        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.options = options

        packages = [Package(u'pgfplots'), Command(u'pgfplotsset',
                                                 u'compat=newest')]

        super(Plot, self).__init__(packages=packages)

    def dumps(self):
        u"""Represent the plot as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        string = Command(u'addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += u' coordinates {\n'

            for x, y in self.coordinates:
                string += u'(' + unicode(x) + u',' + unicode(y) + u')\n'
            string += u'};\n\n'

        elif self.func is not None:
            string += u'{' + self.func + u'};\n\n'

        if self.name is not None:
            string += Command(u'addlegendentry', self.name).dumps()

        super(Plot, self).dumps()

        return string
