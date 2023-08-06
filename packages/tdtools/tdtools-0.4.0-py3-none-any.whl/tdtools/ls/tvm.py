#! /usr/bin/env python

"List Teradata DBC contents"

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

import logging

from tdtools import sqlcsr
from tdtools import util
from tdtools import tdtypes
from tdtools import vsch

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class TVM(tdtypes.DBObj):
	sizefmt = 'Simple'

	def __init__(self, sch, name, typ=None, creator=None, size=None, time=None):
		tdtypes.DBObj.__init__(self, sch, name, typ)
		self.creator, self.size, self.time = creator, util.SSize(size or 0), time

	@staticmethod
	def findall(csr, filter, kind=None, long=False, order=['T.TableName'], reverse=False, hide=None, timecol='LastAlterTimestamp'):
		dbc = vsch.load_schema('dbc')

		def mk_pred(dbtb):
			db, tb = dbtb.split('.') if '.' in dbtb else (dbtb, None)
			dbq = "T.DatabaseName {} '{}'".format('LIKE' if '%' in db else '=', db)
			return dbq if tb == None else "{} AND T.TableName {} '{}'".format(dbq, 'LIKE' if '%' in tb else '=', tb)

		cols = ['T.DatabaseName', 'T.TableName']
		if long:
			cols.extend(['TableKind', 'CreatorName', 'TableSize', timecol])

		tables = ["{dbc.TablesV} T".format(dbc=dbc)]
		if 'TableSize' in cols or 'TableSize' in order:
			tables.append("""(
        SELECT DatabaseName
             , TableName
             , SUM(CurrentPerm) AS TableSize
          FROM {dbc.TableSizeV} Z
         GROUP BY 1,2
       ) Z ON Z.DatabaseName = T.DatabaseName AND Z.TableName = T.TableName""".format(dbc=dbc))

		where = []
		if filter:
			where.append('({})'.format('\n    OR  '.join([mk_pred(dbtb) for dbtb in filter])))
		else:
			where.append('T.DatabaseName = Database')
		if kind:
			where.append('TableKind IN ({})'.format(', '.join(["'{}'".format(k) for k in kind.upper()])))
		if hide:
			where.append('T.TableName NOT LIKE ALL ({})'.format(', '.join(["'{}'".format(p) for p in hide])))

		sql = """\
SELECT {}
  FROM {}
 WHERE {}""".format('\n     , '.join(cols), '\n  LEFT JOIN '.join(tables), '\n   AND '.join(where))

		if order:
			def collate(c):
				desc = c in ['TableSize',timecol,'LastAlterTimestamp']
				if reverse and c != 'TableKind':
					desc = not desc
				return ' DESC' if desc else ''

			sql += "\n ORDER BY " + ', '.join(["{}{}".format(c,collate(c)) for c in order])

		logger.info('About to execute SQL:\n'+ sql)
		csr.execute(sql)

		return [ TVM(*row) for row in csr.fetchall() ]


def main():
	try:
		args = user_args()
		with sqlcsr.cursor(args) as csr:
			return ls(args, csr) or 0
	except Exception as msg:
		logger.exception(msg)

	return 8


def user_args():
	import argparse
	import sys
	import os.path

	cmd = os.path.split(sys.argv[0])[1]
	defkind = {'lstb':'TO','lsvw':'V','lspr':'P','lsji':'I'}.get(cmd)

	p = argparse.ArgumentParser(description = __doc__, add_help=False)

	p.add_argument("names", metavar='OBJECT', nargs='*',                   help="View name or pattern (eg dbc.qry%% dbc.tablesv)")
	p.add_argument(      '--help',    action='help',                       help='show this help message and exit')
	p.add_argument("-D", dest="showdb", action="store_false",              help="Show just the object name without database prefix")
	p.add_argument(      "--kind", metavar='STR', default=defkind,         help="only include TVM entries with specified TableKind")
	p.add_argument("-r", "--reverse", action="store_true",                 help="reverse order while sorting")
	p.add_argument("-l", dest='long', action="store_true",                 help="use a long listing format")
	p.add_argument("-c", dest='timecol', action="store_const", default='LastAlterTimestamp', const='CreateTimestamp', help="sort by, and show, CreateTimestamp")
	p.add_argument("-I", "--hide",    action='append', metavar='PATTERN',  help="do not list implied entries matching PATTERN")
	p.add_argument(      "--group",   action="store_true",                 help="group by object type")

	g = p.add_mutually_exclusive_group()
	g.add_argument("-h", "--human-readable", dest='sizefmt', action="store_const", const='8.1h', default='12', help="with -l, print human readable sizes (e.g., 1K 234M 2G)")
	g.add_argument(      "--si",             dest='sizefmt', action="store_const", const='6.1s', help="likewise, but use powers of 1000 not 1024")

	g = p.add_mutually_exclusive_group()
	g.add_argument(      '--sort', metavar='WORD', default='name', choices=['none','size','name','time'], help="sort by WORD instead of name: none (-U), size (-S), time (-t)")
	g.add_argument("-t", dest='sort', action='store_const', const='mtime', help="sort by modification time, newest first")
	g.add_argument("-U", dest='sort', action='store_const', const='none',  help="do not sort; list entries in database order")
	g.add_argument("-S", dest='sort', action='store_const', const='size',  help="sort by file size, largest first")

	p.add_argument('-v', '--verbose', action='count', default=0,           help='print verbose log information. Use -vv for more details')

	sqlcsr.dbconn_args(p)

	args = p.parse_args()

	if   args.verbose > 1: logger.setLevel(logging.DEBUG)
	elif args.verbose > 0: logger.setLevel(logging.INFO)

	logger.debug('Command name: [{}], Default TableKind: [{}]'.format(cmd, defkind))

	return args


def ls(args, csr):

	if args.sizefmt:
		TVM.sizefmt = args.sizefmt
	if not args.showdb:
		TVM.__str__ = lambda o:str(o.name)

	order = []
	if args.group:
		order.append('TableKind')
	if args.sort:
		if args.sort == 'name' and args.showdb:
			order.append('T.DatabaseName')
		order.append({'size': 'TableSize', 'name':'T.TableName', 'time':args.timecol, 'mtime':'LastAlterTimestamp'}[args.sort])

	objlist = TVM.findall(csr, args.names, kind=args.kind, long=args.long, order=order, reverse=args.reverse, hide=args.hide, timecol=args.timecol)

	if not objlist:
		return

	if args.long:
		c_maxlen = max([len(o.creator) for o in objlist])
		ls_fmt = '{o.objtype} {o.creator:{ol}} {o.size:{sl}} {o.time} {o}'
	else:
		c_maxlen = 0
		ls_fmt = '{o}'

	for o in objlist:
		print(ls_fmt.format(o=o, ol=c_maxlen, sl=args.sizefmt))


if __name__ == '_ls__':
	import sys
	sys.exit(main())
