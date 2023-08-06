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
import time
from qtpy import QtCore


TIMEOUT = 60
active_lang = None
timer = {}
start_time = {}
time_remaining = {}


def on_timeout():
		
	from _actpup import network
	network.send(active_lang)
	time_remaining[active_lang] = TIMEOUT
	resume(active_lang)


def pause():

	global time_remaining
	pause_time = time.time()
	# print('pause_time %s %.2f' % (active_lang, pause_time))
	timer[active_lang].stop()
	time_remaining[active_lang] = pause_time - start_time[active_lang]
	# print('remaining_time %.2f' % time_remaining[active_lang])
	
	
def resume(lang):

	global active_lang
	start_time[lang] = time.time()
	# print('start_time %s %.2f' % (lang, start_time[lang]))
	r = time_remaining.get(lang, TIMEOUT)
	# print('remaining_time %.2f' % r)	
	if lang not in timer:
		timer[lang] = QtCore.QTimer()
		timer[lang].setSingleShot(True)
		timer[lang].timeout.connect(on_timeout)	
	timer[lang].start(1000 * r)
	active_lang = lang
