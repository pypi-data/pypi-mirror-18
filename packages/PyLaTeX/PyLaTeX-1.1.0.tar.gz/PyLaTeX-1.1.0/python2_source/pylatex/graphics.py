# -*- coding: utf-8 -*-
u"""
This module implements the class that deals with graphics.

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
import os.path

from .utils import fix_filename, make_temp_dir, _merge_packages_into_kwargs
from .base_classes import Command, Float
from .package import Package
import uuid


class Figure(Float):

    u"""A class that represents a Figure environment."""

    def __init__(self, *args, **kwargs):
        packages = [Package(u'graphicx')]
        _merge_packages_into_kwargs(packages, kwargs)

        super(Figure, self).__init__(*args, **kwargs)

    def add_image(self, filename, width=ur'0.8\textwidth',
                  placement=ur'\centering'):
        u"""Add an image.to the figure.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        if placement is not None:
            self.append(placement)

        if width is not None:
            width = u'width=' + unicode(width)

        self.append(Command(u'includegraphics', options=width,
                            arguments=fix_filename(filename)))


class SubFigure(Figure):

    u"""A class that represents a subfigure from the subcaption package.

    :param data:
    :param position:

    :type data: list
    :type position: str
    :param data:
    :param position:
    :param seperate_paragraph:

    :type data: list
    :type position: str
    :type seperate_paragraph: bool
    """

    def __init__(self, data=None, position=None, width=ur'0.45\linewidth',
                 seperate_paragraph=False, **kwargs):
        packages = [Package(u'subcaption')]

        super(SubFigure, self).__init__(data=data, packages=packages,
                         position=position,
                         argument=width,
                         seperate_paragraph=seperate_paragraph, **kwargs)

    def add_image(self, filename, width=ur'\linewidth',
                  placement=None):
        u"""Add an image to the subfigure.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        super(SubFigure, self).add_image(filename, width=width, placement=placement)


class MatplotlibFigure(Figure):

    u"""A class that represents a plot created with matplotlib."""

    # TODO: Make an equivalent class for subfigure plots

    container_name = u'figure'

    def __init__(self, *args, **kwargs):
        import matplotlib.pyplot as plt
        self._plt = plt

        super(MatplotlibFigure, self).__init__(*args, **kwargs)

    def _save_plot(self, *args, **kwargs):
        u"""Save the plot.

        :param plt: The matplotlib.pyplot module
        :type plt: matplotlib.pyplot

        :return: The basename with which the plot has been saved.
        :rtype: str
        """

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, unicode(uuid.uuid4()) + u'.pdf')

        self._plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, width=ur'0.8\textwidth',
                 placement=ur'\centering', *args, **kwargs):
        u"""Add a plot.

        :param plt: The matplotlib.pyplot module
        :param width: The width of the plot.
        :param placement: The placement of the plot.

        :type plt: matplotlib.pyplot
        :type width: str
        :type placement: str
        """
        # TODO: Make default width and placement linked to the figure class
        # TODO: Add args and kwargs explanation

        filename = self._save_plot(*args, **kwargs)

        self.add_image(filename, width, placement)
