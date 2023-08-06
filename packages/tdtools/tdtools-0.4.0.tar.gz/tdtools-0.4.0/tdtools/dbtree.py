#! /usr/bin/env python
# -*- coding: utf8 -*-

"List Teradata Database hierarcy"

import logging

from tdtools import sqlcsr
from tdtools import util
from tdtools import vsch

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

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger()

class Dbase(util.Node):
	def __init__(self, parent, name, alloc=0, used=0, peak=0):
		util.Node.__init__(self, parent)
		self.name, self.alloc, self.used, self.peak = name, alloc, used, peak

	@property
	def free(self): return self.alloc - self.used

	def rollup(self, attr):
		return self.__getattribute__(attr) + sum([c.rollup(attr) for c in self.children])


def main():
	try:
		args = user_args()

		sql = build_sql(args.seed, reverse=args.ancestors, get_sizes=args.lslong, max_depth=args.max_depth, dbkind=args.dbkind, non_zero=args.non_zero)
		if args.sql:
			print(sql)
			return

		with sqlcsr.cursor(args) as csr:
			csr.execute(sql)
			tree = build_tree(csr.fetchall() if args.sizefmt else [(d,l,0,0,0) for d,l in csr.fetchall()])

		if tree:
			print_tree(tree, sizefmt=args.sizefmt, size2=args.size2 if args.lslong else None, rollup=args.cumulative, fancy=args.fancy)

		return 0

	except Exception as msg:
		logger.exception(msg)
		return 8


def user_args():
	from argparse import ArgumentParser

	p = ArgumentParser(description = __doc__, add_help=False)

	p.add_argument("seed", metavar='DB', nargs='?', default='dbc', help="database at the root of the hierarchy (default DBC)")
	p.add_argument(      '--help',        action='help',       help='show this help message and exit')
	p.add_argument("-a", "--ancestors",   action='store_true', help="show ancestors instead of descendents")
	p.add_argument("-l", dest='lslong',   action='store_true', help="long list -- show allocated and used database sizes")

	g = p.add_mutually_exclusive_group()
	g.add_argument(      "--free", dest='size2', action="store_const", const='free', default='used', help="likewise, but show free instead of used space")
	g.add_argument(      "--peak", dest='size2', action="store_const", const='peak', help="likewise, but show peak instead of used space")

	p.add_argument("-c", "--cumulative",  action='store_true', help="include child database sizes with parent database sizes")

	g = p.add_mutually_exclusive_group()
	g.add_argument("-h", "--human-readable", dest='sizefmt', action="store_const", const='8.1h', default='18,', help="with -l, print human readable sizes (e.g., 1K 234M 2G)")
	g.add_argument(      "--si",             dest='sizefmt', action="store_const", const='6.1s', help="likewise, but use powers of 1000 not 1024")

	p.add_argument("--max-depth", metavar='INT', type=int,     help="limit hierarchy depth to the specified value")
	p.add_argument("-Z", "--non-zero",    action='store_true', help="only show databases with non-zero PERM space")
	g = p.add_mutually_exclusive_group()
	g.add_argument('-d', '--only-db',   dest='dbkind', action='store_const', const='D', help='list only databases')
	g.add_argument('-u', '--only-users',dest='dbkind', action='store_const', const='U', help='list only users')

	p.add_argument("--sql",               action='store_true', help="show generated SQL; do not run it")
	p.add_argument('-F', '--no-fancy',  dest='fancy', default=True, action='store_false', help='Do not use unicode box characters for drawing')
	p.add_argument('-v', '--verbose',  default=0, action='count', help='print verbose log information. Use -vv for more details')

	sqlcsr.dbconn_args(p)

	args = p.parse_args()

	if   args.verbose > 1: logger.setLevel(logging.DEBUG)
	elif args.verbose > 0: logger.setLevel(logging.INFO)

	return args


def build_sql(root, reverse=False, get_sizes=False, max_depth=None, dbkind=None, non_zero=False):
	dbc = vsch.load_schema('dbc')
	P,C = ('C','P') if reverse else ('P','C') # print top-down or reverse (bottom-up) hierarchy

	where = ['c.CDB is not null', 'p.DB = c.PDB']
	if max_depth:
		where.append("Depth < {}".format(max_depth))
	if dbkind:
		where.append("DBKind = '{}'".format(dbkind))
	if non_zero:
		where.append("PermSpace > 0")

	sql =  """\
with recursive hierarchy(DB, DBPath, Depth, AllocSize) as
(
    select DB
         , cast(DB as varchar(30000))
         , 0
         , PermSpace
      from ancestry s
     where DB = '{}'

     union all

    select c.CDB
         , DBPath || ':' || CDB
         , Depth + 1
         , c.PermSpace
      from ancestry c
         , hierarchy p
     where {}
)

, ancestry as
(
    select DatabaseName          as DB
         , DatabaseName          as {}DB
         , case when DatabaseName = 'DBC'
                then NULL
                else OwnerName
           end                   as {}DB
         , PermSpace
         , DBKind
      from {dbc.DatabasesV}
)
""".format(root, "\n       and ".join(where), C, P, dbc=dbc)

	if get_sizes:

		sql += """
select DB
     , Depth
     , AllocSize
     , UsedSize
     , PeakSize

  from hierarchy h

  join (
        select DatabaseName
             , sum(CurrentPerm) As UsedSize
             , sum(PeakPerm)    As PeakSize
          from {dbc.DiskSpaceV}
         group by 1
       ) z
    on z.DatabaseName = h.DB

 order by DBPath""".format(dbc=dbc)

	else:

		sql += """
select h.DB
     , h.Depth
	 , 0,0,0
  from hierarchy h
 order by DBPath"""

	logger.info('SQL: '+sql)

	return sql


def build_tree(dbinfo):
	prev_level = 0
	root = parent = None

	for name, level, alloc, used, peak in dbinfo:

		if level > prev_level:
			parent = parent.children[-1] if parent else root
		elif level < prev_level:
			parent = parent.parent

		node = Dbase(parent,name,alloc,used,peak)

		if parent:
			parent.children.append(node)
		else:
			root = node

		prev_level = level

	return root


def print_tree(tree, sizefmt=None, size2=None, rollup=False, fancy=True):
	util.Links.set_style(util.Links.fancy if fancy else util.Links.simple)

	if size2 and sizefmt:
		if rollup:
			Dbase.num1 = lambda n: n.rollup('alloc')
			Dbase.num2 = lambda n: n.rollup(size2)
		else:
			Dbase.num1 = lambda n: n.alloc
			Dbase.num2 = lambda n: n.__getattribute__(size2)

		for pfx, node in tree.tree_walk():
			n1, n2 = node.num1(), node.num2()
			pct = n2/n1 if n1 else 0
			print("{:30}  {:{fmt}}  {:{fmt}}  {:4.0%}".format(str(pfx)+node.name, util.SSize(n1), util.SSize(n2), pct, fmt=sizefmt))

	else:
		for pfx, node in tree.tree_walk():
			print(str(pfx)+node.name)


if __name__ == '__main__':
	import sys
	sys.exit(main())
