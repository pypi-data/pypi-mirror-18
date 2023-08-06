# coding=utf-8

"""
This file is part of ActPup.

ActPup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ActPup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ActPup.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from qtpy import QtCore
from QProgEdit.pyqt5compat import Qsci

key_count = {}


def key(name):
	
	return getattr(QtCore.Qt, 'Key_%s' % name)


def key_range(first, last):
	
	return list(range(key(first), key(last)+1))


def keys(*names):
	
	return [key(name) for name in names]
	

key_categories = {
	'alpha'			: key_range('A', 'Z'),
	'_numeric'		: key_range('0', '9'),
	'whitespace'	: keys('Space', 'Tab', 'Enter', 'Return'),
	'_delete'		: keys('Backspace', 'Delete'),
	'navigate'		: keys('Home', 'End', 'Left', 'Up', 'Right', 'Down',
		'PageUp', 'PageDown')
	}


def reset_key_count(lang=None):
	
	key_count[lang] = {'other' : 0}
	for category in key_categories:
		key_count[lang][category] = 0


def key_category(key):
	
	for category, codes in key_categories.items():
		if key in codes:
			return category
	return 'other'


def on_keypress(editor, e):
	
	lang = editor.lang().lower()
	if lang not in key_count:
		reset_key_count(lang)
	key_count[lang][key_category(e.key())]  += 1
	Qsci.QsciScintilla.keyPressEvent(editor, e)
