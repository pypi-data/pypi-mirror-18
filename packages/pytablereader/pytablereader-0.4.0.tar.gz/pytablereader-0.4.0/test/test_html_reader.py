# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import collections
import os

import pytest

import pytablereader as ptr
from pytablereader.interface import TableLoader
from pytablereader.data import TableData
from pytablereader.html.formatter import HtmlTableFormatter


Data = collections.namedtuple("Data", "value expected")

test_data_empty = Data(
    """[]""",
    [
        TableData("tmp", [], []),
    ])

test_data_01 = Data(
    """<table>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
  </tbody>
</table>
""",
    [
        TableData(
            table_name=u"html1",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
    ])

test_data_02 = Data(
    """<table id="tablename">
    <caption>caption</caption>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
</table>
""",
    [
        TableData(
            table_name=u"tablename",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
    ])

test_data_03 = Data(
    """
<html>
  <head>
    header
  </head>
  <body>
    hogehoge
  </body>
</html>
""",
    [])

test_data_04 = Data(
    """
<table id="tablename">
    <caption>caption</caption>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
</table>
<table>
</table>
<table>
    <tr></tr>
    <tr></tr>
</table>
<table>
    <tr>
      <th>a</th>
      <th>b</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
    </tr>
</table>
""",
    [
        TableData(
            table_name=u"tmp_tablename",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
        TableData(
            table_name=u"tmp_html2",
            header_list=[u'a', u'b'],
            record_list=[
                [u'1', u'123.1'],
                [u'2', u'2.2'],
                [u'3', u'3.3'],
            ]
        ),
    ])


test_data_05 = Data(
    """<table>
  <caption>captiontest</caption>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
  </tbody>
</table>
""",
    [
        TableData(
            table_name=u"tmp_captiontest",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
    ])


test_data_06 = Data(
    """
<table class="prettytable inflection-table">
<tr>
<th style="background:#549EA0; font-style:italic;">Case</th>
<th style="background:#549EA0; font-style:italic;">Singular</th>
<th style="background:#549EA0; font-style:italic;">Plural</th>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/nominative_case" title="nominative case">nominative</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><strong class="selflink">val01</strong></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythones#Latin" title="pythones">val02</a></span></td>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/genitive_case" title="genitive case">genitive</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonis#Latin" title="pythonis">val11</a></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonum#Latin" title="pythonum">val12</a></span></td>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/dative_case" title="dative case">dative</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythoni#Latin" title="pythoni">val21</a></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonibus#Latin" title="pythonibus">val22</a></span></td>
</tr>
</table>
""",
    [
        TableData(
            table_name="tmp_html1",
            header_list=["Case", "Singular", "Plural"],
            record_list=[
                ["nominative", "val01", "val02"],
                ["genitive", "val11", "val12"],
                ["dative", "val21", "val22"],
            ]
        ),
    ])


class HtmlTableFormatter_constructor(object):

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["tablename", None, ptr.InvalidDataError],
        ["tablename", "", ptr.InvalidDataError],
    ])
    def test_exception(
            self, monkeypatch, value, source, expected):
        with pytest.raises(expected):
            HtmlTableFormatter(source)


class Test_HtmlTableFormatter_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @property
    def valid_tag_property(self):
        return "htmltable"

    @property
    def null_tag_property(self):
        return None

    FILE_LOADER_TEST_DATA = [
        ["%(filename)s", "/path/to/data.html", "data"],
        ["prefix_%(filename)s",  "/path/to/data.html", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.html", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.html",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.html",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.html",
            "html0_data"
        ],
    ]

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s",  "/path/to/data.html", "data_htmltable"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_HtmlTableFileLoader_valid_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s",  "/path/to/data.html", "data_html0"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_HtmlTableFileLoader_null_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.html", ValueError],
        ["", "/path/to/data.html", ValueError],
        [
            "%(%(filename)s)",
            "/path/to/data.html",
            ptr.InvalidTableNameError  # %(data)
        ],
    ])
    def test_HtmlTableFileLoader_exception(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            formatter._make_table_name()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "htmltable"],
        ["%(key)s", "htmltable"],
        ["%(format_name)s%(format_id)s", "html0"],
        ["%(filename)s%(format_name)s%(format_id)s", "html0"],
        ["tablename", "tablename"],
        ["table", "table_html"],
    ])
    def test_normal_HtmlTableTextLoader_valid_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        source = "<table></table>"
        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "html0"],
        ["%(key)s", "html0"],
        ["%(format_name)s%(format_id)s", "html0"],
        ["%(filename)s%(format_name)s%(format_id)s", "html0"],
        ["tablename", "tablename"],
        ["table", "table_html"],
    ])
    def test_normal_HtmlTableTextLoader_null_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        source = "<table></table>"
        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "<table></table>", ValueError],
        [
            "%(filename)s",
            "<table></table>",
            ptr.InvalidTableNameError
        ],
    ])
    def test_exception_HtmlTableTextLoader(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            print(formatter._make_table_name())


class Test_HtmlTableFileLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "filename",
            "table_name",
            "expected_tabledata_list",
        ],
        [
            [
                1, test_data_01.value, "tmp.html",
                "%(key)s",
                test_data_01.expected
            ],
            [
                2, test_data_02.value, "tmp.html",
                "%(key)s",
                test_data_02.expected,
            ],
            [
                3, test_data_03.value, "tmp.html",
                "%(default)s",
                test_data_03.expected,
            ],
            [
                4, test_data_04.value, "tmp.html",
                "%(default)s",
                test_data_04.expected,
            ],
            [
                5, test_data_05.value, "tmp.html",
                "%(default)s",
                test_data_05.expected,
            ],
            [
                6, test_data_06.value, "tmp.html",
                "%(default)s",
                test_data_06.expected,
            ],
        ])
    def test_normal(
            self, tmpdir, test_id, table_text, filename,
            table_name, expected_tabledata_list):
        p_file_path = tmpdir.join(filename)

        parent_dir_path = os.path.dirname(str(p_file_path))
        if not os.path.isdir(parent_dir_path):
            os.makedirs(parent_dir_path)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = ptr.HtmlTableFileLoader(str(p_file_path))
        loader.table_name = table_name

        for tabledata, expected in zip(loader.load(), expected_tabledata_list):
            print("[test {}]".format(test_id))
            print("actual: {}".format(tabledata.dumps()))
            print("expected:  {}".format(expected.dumps()))
            print("")
            assert tabledata == expected

    @pytest.mark.parametrize(
        [
            "table_text",
            "filename",
            "expected",
        ],
        [
            [
                "",
                "tmp.html",
                ptr.InvalidDataError,
            ],
        ])
    def test_exception_invalid_data(
            self, tmpdir, table_text, filename, expected):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = ptr.HtmlTableFileLoader(str(p_file_path))

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(["filename", "expected"], [
        ["", IOError],
        [None, IOError],
    ])
    def test_exception_null_filename(
            self, tmpdir, filename, expected):
        loader = ptr.HtmlTableFileLoader(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_HtmlTableTextLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "table_text",
            "table_name",
            "expected_tabletuple_list",
        ],
        [
            [
                test_data_01.value,
                "%(default)s",
                test_data_01.expected,
            ],
            [
                test_data_02.value,
                "%(default)s",
                test_data_02.expected,
            ],
            [
                test_data_03.value,
                "%(default)s",
                test_data_03.expected,
            ],
        ])
    def test_normal(self, table_text, table_name, expected_tabletuple_list):
        loader = ptr.HtmlTableTextLoader(table_text)
        loader.table_name = table_name

        for tabletuple in loader.load():
            assert tabletuple in expected_tabletuple_list

    @pytest.mark.parametrize(["table_text", "expected"], [
        ["", ptr.InvalidDataError],
        [None, ptr.InvalidDataError],
    ])
    def test_exception_null(self, table_text, expected):
        loader = ptr.HtmlTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
