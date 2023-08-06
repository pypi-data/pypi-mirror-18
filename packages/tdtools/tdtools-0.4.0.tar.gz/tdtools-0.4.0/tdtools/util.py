"Teradata utility functions"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016, Paresh Adhia"
__license__ = "GPL"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

class EnhancedCursor:
	"Cursor wrapper class with some useful attributes"

	_version = None

	def __init__(self, csr):
		self.csr = csr

	@property
	def version(self):
		if not EnhancedCursor._version:
			self.csr.execute("Select InfoData From DBC.DBCInfoV Where InfoKey = 'VERSION'")
			EnhancedCursor._version = self.csr.fetchone()[0]
		return EnhancedCursor._version

	@property
	def schema(self):
		self.execute('select database')
		return self.fetchone()[0]

	@schema.setter
	def schema(self, new_schema):
		import sqlcsr

		self.execute('database ' + new_schema)
		sqlcsr.commit()

	def fetchxml(self):
		import re

		val, rows = '', self.fetchmany(100)
		while rows:
			for row in rows:
				val += row[0]
			rows = self.fetchmany(100)

		val = re.sub('xmlns=".*?"','',re.sub('encoding="UTF-16"','encoding="utf-8"',val,1,flags=re.IGNORECASE),1)

		return val

	def __getattr__(self,attr):  return getattr(self.csr,attr)

# Classes to represent (object/database) hierarchy
class Links:
	fancy  = {'T':"├─ ", 'L':"└─ ", 'I':"│  ", ' ':"   "}
	simple = {'T':"|- ", 'L':"L_ ", 'I':"|  ", ' ':"   "}

	style = fancy

	@staticmethod
	def set_style(style):
		Links.style = style

	def __init__(self, chain=''):
		self.chain = chain

	def extend(self,ch):
		return Links(self.chain.replace('L',' ').replace('T','I') + ch)

	def __str__(self):
		return ''.join([self.style[k] for k in self.chain])


class Node:
	def __init__(self, parent):
		self.parent, self.children = parent, []

	def tree_walk(self, pfx=Links()):
		yield (pfx,self)

		if self.children:
			for c in self.children[:-1]:
				yield from c.tree_walk(pfx.extend('T'))
			yield from self.children[-1].tree_walk(pfx.extend('L'))


# Class for formatting Storage Size
class SSize(int):
	def __format__(self, spec):
		m = re.match('(\d*)(.\d+)?(h|s|e)$',spec)
		if not m:
			return int.__format__(self, spec)

		width, prec, typ = m.groups()

		if typ == 'e':
			if prec:
				raise ValueError('Precision not allowed in integer format specifier')

			if self == 0:
				s = '0'
			else:
				for e in [12,9,6,3,0]:
					if self % 10**e == 0:
						break
				s = (str(self // 10**e) + 'e' + str(e)) if e else str(self)

		else:
			num = float(self)
			base = 1000.0 if spec[-1] == 's' else 1024.0

			for unit in ['','K','M','G','T','P','E','Z','Y']:
				if num < base:
					break
				num /= base

			fmt = ',' + (prec or '.0') + 'f'
			s = format(num,fmt).rstrip('0').rstrip('.') + unit

		return s.rjust(int(width)) if width else s


def load_json(resource):
	import json
	from pkg_resources import resource_filename

	with open(resource_filename(__name__,resource),'r') as jsonf:
		return json.load(jsonf)
