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
from QProgEdit import QEditor
from _actpup import timer


def inject():
		
	QEditor._focusInEvent = QEditor.focusInEvent
	QEditor.focusInEvent = on_focus_in
	QEditor._focusOutEvent = QEditor.focusOutEvent
	QEditor.focusOutEvent = on_focus_out
		
		
def on_focus_in(editor, e):
	
	timer.resume(editor.lang().lower())
	QEditor._focusInEvent(editor, e)


def on_focus_out(editor, e):
	
	timer.pause()
	QEditor._focusInEvent(editor, e)
