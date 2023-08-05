# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from .._validator import FileValidator
from .._validator import TextValidator
from ..interface import TableLoader
from .formatter import HtmlTableFormatter


class HtmlTableLoader(TableLoader):
    """
    Abstract class of HTML table loader.
    """

    @property
    def format_name(self):
        return "html"


class HtmlTableFileLoader(HtmlTableLoader):
    """
    Concrete class of HTML file loader.

    :param str file_path: Path to the loading HTML file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    def __init__(self, file_path=None):
        super(HtmlTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract |TableData| from HTML table tags in a HTML file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute is not included
                                 | in the table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the HTML data is invalid or empty.

        .. note::

            Table tag attributes are ignored with loaded |TableData|.
        """

        self._validate()

        formatter = None
        with open(self.source, "r") as fp:
            formatter = HtmlTableFormatter(fp.read())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.FILENAME, tnt.KEY)


class HtmlTableTextLoader(HtmlTableLoader):
    """
    Concrete class of HTML text loader.

    :param str text: HTML text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    def __init__(self, text):
        super(HtmlTableTextLoader, self).__init__(text)

        self._validator = TextValidator(text)

    def load(self):
        """
        Extract |TableData| from HTML table tags in a HTML text.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute is not included
                                 | in the table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the HTML data is invalid or empty.
        """

        self._validate()

        formatter = HtmlTableFormatter(self.source)
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}".format(tnt.KEY)
