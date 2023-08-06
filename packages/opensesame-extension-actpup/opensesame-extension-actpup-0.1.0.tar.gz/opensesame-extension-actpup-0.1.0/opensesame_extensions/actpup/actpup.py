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
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import base_extension
from QProgEdit import QEditor
from _actpup import lexer, network, focus, timer, key


class actpup(base_extension):
		
	def event_startup(self):
		
		if cfg.actpup_id:
			self.start()
			return
		self.tabwidget.open_markdown(self.ext_resource('start.md'),
			u'applications-science', u'Thank you!')
			
	def set_expertise(self, expertise):
		
		cfg.actpup_expertise = expertise
		self.tabwidget.close_current()
		self.generate_id()
		self.start()
		
	def generate_id(self):
		
		import uuid
		cfg.actpup_id = uuid.uuid1()
		
	def start(self):

		if not network.register(cfg.actpup_id, cfg.actpup_expertise):
			return
		focus.inject()
		lexer.inject()
		QEditor.keyPressEvent = key.on_keypress
		self.extension_manager.fire(u'notify', message=u'Thank you for '
			u'participating in ActPup! You can disable the actpup '
			u'extension to stop.')
					
	def event_run_experiment(self, fullscreen):
		
		timer.pause()

	def event_end_experiment(self, ret_val):
		
		timer.resume()

	def event_actpup_expertise_0(self): self.set_expertise(0)
	def event_actpup_expertise_1(self): self.set_expertise(1)
	def event_actpup_expertise_2(self): self.set_expertise(2)
