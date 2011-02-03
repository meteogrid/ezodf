#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test table
# Created: 20.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import CN, etree, wrap

# objects to test
from ezodf.cells import Cell
from ezodf.table import Table, address_to_index

TESTTABLE = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" />
"""

class TestTableAttributes(unittest.TestCase):
    def test_has_TAG(self):
        table = Table()
        self.assertEqual(table.TAG, CN('table:table'))

    def test_has_xmlnode(self):
        table = Table()
        self.assertIsNotNone(table.xmlnode)

    def test_get_name(self):
        table = Table()
        name = table.name
        self.assertTrue(isinstance(name, str))

    def test_set_name(self):
        table = Table()
        table.name = 'TABLE'
        self.assertEqual(table.name, 'TABLE')
        self.assertEqual(table.get_attr(CN('table:name')), 'TABLE', 'wrong tag name')

    def test_get_style_name(self):
        table = Table()
        self.assertIsNone(table.style_name)

    def test_set_style_name(self):
        table = Table()
        table.style_name = 'STYLE'
        self.assertEqual(table.style_name, 'STYLE')
        self.assertEqual(table.get_attr(CN('table:style-name')), 'STYLE', 'wrong tag name')

    def test_get_protected(self):
        table = Table()
        self.assertFalse(table.protected)

    def test_set_protected(self):
        table = Table()
        table.protected = True
        self.assertTrue(table.protected)
        self.assertEqual(table.get_attr(CN('table:protected')), 'true', 'wrong tag name')

    def test_protection_key_not_set(self):
        table = Table()
        key = table.get_attr(CN('table:protection-key'))
        self.assertIsNone(key)

    def test_protection_key_is_set(self):
        table = Table()
        table.protected = True
        key = table.get_attr(CN('table:protection-key'))
        self.assertIsNotNone(key, "protection-key not set")
        self.assertGreater(len(key), 8, "protection-key is too short")

    def test_get_print(self):
        table = Table()
        self.assertFalse(table.print)

    def test_set_print(self):
        table = Table()
        table.print = True
        self.assertTrue(table.print)
        self.assertEqual(table.get_attr(CN('table:print')), 'true', 'wrong tag name')

    def test_if_Table_class_is_registered(self):
        table = wrap(etree.XML(TESTTABLE))
        self.assertEqual(table.TAG, CN('table:table'), 'Table class is not registered')

TABLE_5x3 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
<table:table-row><table:table-cell /><table:table-cell /><table:table-cell /></table:table-row>
</table:table>
"""

TABLE_REP_7x7 = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-row><table:table-cell table:number-columns-repeated="7"/></table:table-row>
<table:table-row table:number-rows-repeated="6"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
</table:table>
"""

class TestTableMethods(unittest.TestCase):
    def test_nrows(self):
        table = wrap(etree.XML(TABLE_5x3))
        self.assertEqual(table.nrows(), 5)

    def test_nrows_repeated(self):
        table = wrap(etree.XML(TABLE_REP_7x7))
        self.assertEqual(table.nrows(), 7)

    def test_ncols(self):
        table = wrap(etree.XML(TABLE_5x3))
        self.assertEqual(table.ncols(), 3)

    def test_ncols_repeated(self):
        table = wrap(etree.XML(TABLE_REP_7x7))
        self.assertEqual(table.ncols(), 7)

    def test_init_row_cols(self):
        table = Table(name="TEST", size=(7, 5))
        self.assertEqual(table.nrows(), 7)
        self.assertEqual(table.ncols(), 5)

    def test_clear(self):
        table = Table(name="TEST", size=(7, 5))
        table.clear(size=(8, 10))
        self.assertIsNone(table.name)
        self.assertEqual(table.ncols(), 10)
        self.assertEqual(table.nrows(), 8)

    def test_setup_error(self):
        with self.assertRaises(ValueError):
            Table(size=(1, 0))
        with self.assertRaises(ValueError):
            Table(size=(0, 1))

class TestAddress2Index(unittest.TestCase):
    def test_A1(self):
        self.assertEqual(address_to_index('A1'), (0, 0))

    def test_A2(self):
        self.assertEqual(address_to_index('A2'), (1, 0))

    def test_C2(self):
        self.assertEqual(address_to_index('C2'), (1, 2))

    def test_AA100(self):
        self.assertEqual(address_to_index('AA100'), (99, 26))

    def test_CCC100(self):
        self.assertEqual(address_to_index('CCC100'), (99, 2108))

    def test_errors(self):
        with self.assertRaises(ValueError):
            address_to_index('100')
        with self.assertRaises(ValueError):
            address_to_index('A')
        with self.assertRaises(ValueError):
            address_to_index('a1')
        with self.assertRaises(ValueError):
            address_to_index('A1A')

TABLE_COMP = """
<table:table xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
<table:table-row><table:table-cell table:number-columns-repeated="7"/></table:table-row>
<table:table-row table:number-rows-repeated="6"><table:table-cell table:number-columns-repeated="7" /></table:table-row>
</table:table>
"""

class TestTableContent(unittest.TestCase):
    def setUp(self):
        self.table = Table(xmlnode=etree.XML(TABLE_COMP))

    def test_metrics(self):
        self.assertEqual(self.table.ncols(), 7)
        self.assertEqual(self.table.nrows(), 7)

    def test_set_get_different_values(self):
        ncols = self.table.ncols()
        for row in range(self.table.nrows()):
            for col in range(ncols):
                cell = self.table[row, col]
                cell.set_value(row*ncols + col, 'float')

        for row in range(self.table.nrows()):
            for col in range(ncols):
                cell = self.table[row, col]
                self.assertEqual(row*ncols + col, int(cell.value))


SQUAREMATRIX = """
<table:table
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 table:name="RowColAccess">

<table:table-columns>
  <table:table-column table:style-name="c0" />
  <table:table-column table:style-name="c1" />
  <table:table-column table:style-name="c2" />
  <table:table-column table:style-name="c3" />
</table:table-columns>

<table:table-rows>
  <table:table-row table:style-name='r0'>
    <table:table-cell office:value-type="float" office:value="1" />
    <table:table-cell office:value-type="float" office:value="2" />
    <table:table-cell office:value-type="float" office:value="3" />
    <table:table-cell office:value-type="float" office:value="4" />
  </table:table-row>
  <table:table-row table:style-name='r1'>
    <table:table-cell office:value-type="float" office:value="5" />
    <table:table-cell office:value-type="float" office:value="6" />
    <table:table-cell office:value-type="float" office:value="7" />
    <table:table-cell office:value-type="float" office:value="8" />
  </table:table-row>
  <table:table-row table:style-name='r2'>
    <table:table-cell office:value-type="float" office:value="9" />
    <table:table-cell office:value-type="float" office:value="10" />
    <table:table-cell office:value-type="float" office:value="11" />
    <table:table-cell office:value-type="float" office:value="12" />
  </table:table-row>
  <table:table-row table:style-name='r3'>
    <table:table-cell office:value-type="float" office:value="13" />
    <table:table-cell office:value-type="float" office:value="14" />
    <table:table-cell office:value-type="float" office:value="15" />
    <table:table-cell office:value-type="float" office:value="16" />
  </table:table-row>
</table:table-rows>
</table:table>
"""

class TestTableContentAccess(unittest.TestCase):
    def setUp(self):
        self.table = Table(xmlnode=etree.XML(SQUAREMATRIX))

    def test_metrics(self):
        self.assertEqual(self.table.name, 'RowColAccess')
        self.assertEqual(self.table.ncols(), 4)
        self.assertEqual(self.table.nrows(), 4)

    def test_row_neg_index(self):
        cell = self.table[-1, 0]
        self.assertEqual(cell.value, 13.)

    def test_col_index_error(self):
        with self.assertRaises(IndexError):
            self.table[0, 4]

    def test_access_cell_by_index(self):
        cell = self.table[0, 0]
        self.assertEqual(cell.value, 1.)

    def test_access_cell_by_reference(self):
        cell = self.table['B1']
        self.assertEqual(cell.value, 2.)

    def test_setting_cell_by_index(self):
        self.table[0, 0] = Cell('Textcell')
        cell = self.table['A1']
        self.assertEqual(cell.plaintext(), "Textcell")

    def test_setting_cell_by_address(self):
        self.table['A1'] = Cell('Textcell')
        cell = self.table[0, 0]
        self.assertEqual(cell.plaintext(), "Textcell")

    def test_set_cell_row_index_error(self):
        with self.assertRaises(IndexError):
            self.table[10, 0] = Cell()

    def test_set_cell_column_index_error(self):
        with self.assertRaises(IndexError):
            self.table[0, 10] = Cell()

    def test_set_cell_neg_row_index(self):
        self.table[-1, 0] = Cell('Textcell')
        cell = self.table[3, 0]
        self.assertEqual(cell.plaintext(), "Textcell")

    def test_set_cell_neg_column_index(self):
        self.table[0, -1] = Cell('Textcell')
        cell = self.table[0, 3]
        self.assertEqual(cell.plaintext(), "Textcell")

    def test_iter_rows(self):
        nrows = self.table.nrows()
        ncols = self.table.ncols()
        for row in self.table.rows():
            cells = list(row)
            self.assertEqual(len(cells), ncols)
            nrows -= 1
        self.assertEqual(nrows, 0)


class TestRowColumnAccess(unittest.TestCase):
    def setUp(self):
        self.table = Table(xmlnode=etree.XML(SQUAREMATRIX))

    def test_get_row_1_by_index(self):
        values = [cell.value for cell in self.table.row(1)]
        self.assertEqual(values, [5., 6., 7., 8.])

    def test_get_row_1_by_address(self):
        values = [cell.value for cell in self.table.row('A2')]
        self.assertEqual(values, [5., 6., 7., 8.])

    def test_row_index_error(self):
        with self.assertRaises(IndexError):
            self.table.row(4)

    def test_row_neg_index(self):
        values = [cell.value for cell in self.table.row(-1)]
        self.assertEqual(values, [13., 14., 15., 16.])

    def test_get_column_1_by_index(self):
        values = [cell.value for cell in self.table.column(1)]
        self.assertEqual(values, [2., 6., 10., 14.])

    def test_get_column_1_by_address(self):
        values = [cell.value for cell in self.table.column('B2')]
        self.assertEqual(values, [2., 6., 10., 14.])

    def test_column_index_error(self):
        with self.assertRaises(IndexError):
            self.table.column(4)

    def test_column_neg_index(self):
        values = [cell.value for cell in self.table.column(-1)]
        self.assertEqual(values, [4., 8., 12., 16.])

class TestRowColumnInfoAccess(unittest.TestCase):
    def setUp(self):
        self.table = Table(xmlnode=etree.XML(SQUAREMATRIX))

    def test_get_row_info(self):
        row_info = self.table.row_info(0)
        self.assertEqual(row_info.style_name, 'r0')

    def test_get_row_info_by_address(self):
        row_info = self.table.row_info('C2')
        self.assertEqual(row_info.style_name, 'r1')

    def test_get_row_info_neg_index(self):
        row_info = self.table.row_info(-1)
        self.assertEqual(row_info.style_name, 'r3')

    def test_get_row_info_index_error(self):
        with self.assertRaises(IndexError):
            self.table.row_info(4)

    def test_get_column_info(self):
        column_info = self.table.column_info(0)
        self.assertEqual(column_info.style_name, 'c0')

    def test_get_column_info_by_address(self):
        column_info = self.table.column_info('B3')
        self.assertEqual(column_info.style_name, 'c1')

    def test_get_column_info_neg_index(self):
        column_info = self.table.column_info(-1)
        self.assertEqual(column_info.style_name, 'c3')

    def test_get_column_info_index_error(self):
        with self.assertRaises(IndexError):
            self.table.column_info(4)

if __name__=='__main__':
    unittest.main()