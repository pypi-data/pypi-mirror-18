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

import random
from libopensesame.py3compat import *
from QProgEdit._qlexer import QBaseLexer
from QProgEdit import _qcolorscheme
from _actpup import colorschemes

scheme = None


def set_theme(self, editor, colorScheme):
	
	QBaseLexer._setTheme(self, editor, scheme)


def inject():
	
	global scheme
	
	scheme = random.choice( [
		u'material_dark_hi',
		u'material_bright_hi',
		u'material_dark_lo',
		u'material_bright_lo',
		] )
	setattr(_qcolorscheme, scheme, getattr(colorschemes, scheme))
	QBaseLexer._setTheme = QBaseLexer.setTheme
	QBaseLexer.setTheme = set_theme
