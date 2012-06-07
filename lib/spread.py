# spread.py
# The spreadsheet library for Python
#
# Copyright 2012 Florent Gallaire <fgallaire@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import string
from math import *

# LibreOffice compatibility
SIN = sin
COS = cos
TAN = tan
ASIN = asin
ACOS = acos
ATAN = atan
SINH = sinh
COSH = cosh
TANH = tanh


class SpreadSheet:
    """Raymond Hettinger's recipe
    http://code.activestate.com/recipes/355045-spreadsheet
    """
    _cells = {}
    def __setitem__(self, key, formula):
        self._cells[key] = formula
    def getformula(self, key):
        return self._cells[key]
    def __getitem__(self, key):
        if self._cells[key].strip()[0] == '=':
            try:
                return eval(self._cells[key].strip()[1:], globals(), self)
            except Exception, e:
                return e
        else:
            return self._cells[key].strip()


def spreadsheet(data, markup):
    n = max([len(line[0]) for line in data])
    if n > 676:
        Error("Spreadsheet tables are limited to 676 columns, and your table has %i columns." % n)
    s = SpreadSheet()
    for j, row in enumerate(data):
        for i, el in enumerate(row[0]):
            ind = string.ascii_uppercase[i/26 - 1].replace('Z', '') + string.ascii_uppercase[i%26] + str(j+1)
            if el and el.strip():
                s[ind] = el
    for j, row in enumerate(data):
        for i, el in enumerate(row[0]):
            ind = string.ascii_uppercase[i/26 - 1].replace('Z', '') + string.ascii_uppercase[i%26] + str(j+1)
            if el and el.strip():
                if markup == 'html':
                    row[0][i] = '<a title="' + el.strip() + '">' + str(s[ind]) + '</a>'
                elif markup == 'tex':
                    if el.strip()[0] == '=':
                        tooltip = 'formula: '
                    else:
                        tooltip = 'value: '
                    row[0][i] = '\htmladdnormallink{' + str(s[ind]) + '}{' + tooltip + el.strip() + '}'
                elif markup == 'txt':
                    row[0][i] = str(s[ind])
    h = [(string.ascii_uppercase[i/26 - 1].replace('Z', '') + string.ascii_uppercase[i%26]) for i in range(n)]
    data = [[h, [1] * n]] + data
    data = [[[str(i)] + line[0], [1] + line[1]] for i, line in enumerate(data)]
    data[0][0][0] = ''
    return data


def completes_table(table):
    data = [[row['cells'], row['cellspan']] for row in table]
    n = max([len(line[0]) for line in data])
    data2 = []
    for line in data:
        if not line[1]:
            data2.append([n * [''], n * [1]])
        else:
            data2.append([line[0] + (n - sum(line[1])) * [''], line[1] + (n - sum(line[1])) * [1]])
    return data2
