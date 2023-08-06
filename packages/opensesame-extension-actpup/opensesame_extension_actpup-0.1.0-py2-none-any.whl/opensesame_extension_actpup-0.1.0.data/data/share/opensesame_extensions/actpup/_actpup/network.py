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
from _actpup import key, lexer, timer
if py3:
	from urllib.parse import urlencode
	from urllib.request import urlopen
else:
	from urllib import urlencode
	from urllib2 import urlopen
import json
	
URL_SEND = 'http://www.cogsci.nl/files/software/actpup/log.php?'
URL_REGISTER = 'http://www.cogsci.nl/files/software/actpup/register.php?'

_uuid = None
_expertise = None


def read(url):
	
	# print('reading', url)
	fd = urlopen(url)
	response = fd.read()
	# print('response', response)
	fd.close()
	try:
		return json.loads(response)
	except ValueError:
		return { 'status' : 'error', 'message' : 'failed to decode json' }


def register(uuid, expertise):
	
	global _uuid, _expertise
	_uuid = uuid
	_expertise = expertise
	url = URL_REGISTER + urlencode({'uuid' : uuid, 'expertise' : expertise})
	d = read(url)
	return 'status' in d and d['status'] == 'ok'


def send(lang):
	
	if lang not in key.key_count:
		key.reset_key_count(lang)
	d = key.key_count[lang]
	d['lang'] = lang
	d['uuid'] = _uuid
	d['scheme'] = lexer.scheme
	d['timeout'] = timer.TIMEOUT
	url = URL_SEND + urlencode(d)
	read(url)
	key.reset_key_count(lang)
