#! /usr/bin/env python

"Generate TPT script to load Teradata table(s)"

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import os.path
from glob import glob

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
logger = logging.getLogger(__name__)

size_thresholds = [1e6, 1e9, 10e9]

class Err(Exception): pass

class Target:
	def __init__(self, name, seq=None, size=None, tempdb=None):
		self.name, self.size, self.sfx = name, size, '_{0}'.format(seq) if seq else ''

		if tempdb:
			tbname = name.split('.')[1] if '.' in name else name
			self.rlog, self.err1, self.err2 = ["@UtilDatabase || '.{1}_{2}'".format(tempdb, tbname, sfx) for sfx in ['RL','ET','UV']]

		logger.debug('Table:%s' % self.name)

	@property
	def src(self):
		return Target.tgt2src(self.name)

	@staticmethod
	def tgt2src(tgt):
		return tgt


class DBTarget(Target):
	def __init__(self, name, seq=None, size=None, tempdb=None):
		Target.__init__(self, name, seq=seq, size=size or 'MEDIUM', tempdb=tempdb)


class FileTarget(Target):
	def __init__(self, name, seq=None, size=None, tempdb=None):
		Target.__init__(self, name, seq=seq, size=size, tempdb=tempdb)

		self.files = glob(self.src)

		if self.size == None:

			if not self.files:
				logger.warn('No data file(s) [%s] exist for table: [%s].' % (self.src, self.name))
				self.size = 'MEDIUM'

			else:
				logger.info('Table:%s, File(s)=%s' % (self.name, ','.join(self.files)))
				if self.size == None:
					fsize = sum([os.path.getsize(f) for f in self.files])
					self.size = 'LARGE'
					for e,l in enumerate(size_thresholds):
						if fsize < l:
							self.size = ['TINY','SMALL','MEDIUM'][e]
							break
					logger.info('Table:%s, Filesize: %d, TPT Data-size: %s' % (self.name, fsize, self.size))


class TPTVar:
	var_maxlen = 0

	def __init__(self, var, val):
		self.var, self.val = var, val
		if TPTVar.var_maxlen < len(self.var):
			TPTVar.var_maxlen = len(self.var)

	def __str__(self):
		return 'SET {0:{1}} = {2};'.format(self.var, TPTVar.var_maxlen, TPTVar._format_val(self.val))

	@staticmethod
	def _format_val(val):
		if isinstance(val, int):  return "{0}".format(val)
		if isinstance(val, list): return '[' + ','.join([TPTVar._format_val(v) for v in val]) + ']'
		if val[0] == '@':         return val

		return "'{0}'".format(val)

def indent(text):
	return text.replace('\n','\n    ')

class TPTStep:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return """\
STEP {0} (
    APPLY {1}
);""".format(self.name, indent(self.strop()))


class ApplyDDL(TPTStep):
	def __init__(self, name, ddls):
		TPTStep.__init__(self,name)
		self.ddls = ddls if isinstance(ddls,list) else ['(' + ddls + ')']

	def strop(self): return """{0}
    TO OPERATOR ($DDL ATTR(QueryBandSessInfo='{args.qb}TPTJobId=' || $JOBID || ';'));""".format('\n    , '.join(self.ddls), args=args)


class ApplyLoad(TPTStep):
	def __init__(self, tb):
		TPTStep.__init__(self,'LoadTbl{0}'.format(tb.sfx))
		self.tb = tb

	def cop(self):
		op = '$STREAM' if self.tb.size == 'TINY' else '$LOAD'

		if args.cinst:
			op += '[@CInstances]'
		elif not args.odbc and not args.td and round(len(self.tb.files) / 4) > 1:
			op += '[{0}]'.format(int(round(len(self.tb.files) / 4)))

		attr = []

		if op.startswith('$LOAD'):
			attr.extend(["TargetTable='{tb.name}'", "QueryBandSessInfo='{args.qb}TPTJobId=' || $JOBID || ';UtilityDataSize={tb.size};'"])
		else:
			attr.extend(["QueryBandSessInfo='{args.qb}TPTJobId=' || $JOBID || ';'"])

		if args.tempdb:
			attr.append("LogTable={tb.rlog}")
			if op.startswith('$LOAD'):
				attr.extend(["ErrorTable1={tb.err1}", "ErrorTable2={tb.err2}"])
			else:
				attr.append("ErrorTable={tb.err1}")

		if attr:
			op += " ATTR( {0} )".format(',\n                      '.join(attr).format(tb=self.tb,args=args))

		return op

	def pop(self,db=None):

		if args.td or args.odbc :
			op = "$EXPORT('{tb.name}')".format(tb=self.tb) if args.td else "$ODBC"
			if args.pinst:
				op += '[@PInstances]'
			op += " ATTR(SelectStmt='Lock Row Access Select * From {tb.src}')".format(tb=self.tb)

		else:
			op = "$FILE_READER({0}'{tb.name}')".format('DELIMITED ' if not args.binary else '',tb=self.tb)

			if args.pinst:
				op += '[@PInstances]'
			elif len(self.tb.files) > 1:
				op += '[{0}]'.format(len(self.tb.files))

			multi_reader = len(self.tb.files) >= 1 and args.pinst and args.pinst > len(self.tb.files) # Enable multiple readers if producer instances > # of files.
			op += " ATTR(FileName='{tb.src}'" + (", MultipleReaders='Yes'" if multi_reader else "") + ")"
			op = op.format(db+'.' if db else '', tb=self.tb)

		return op

	def strop(self):
		if args.null == '' or len([c for c in self.tb.cols if c.nul]) == 0: # if empty-string is null or there are no nullable columns
			ins = "$INSERT '{tb.name}'".format(tb=self.tb)
			cols = '*'
		else:
			ins = "'INSERT INTO {tb.name} ({tb.hlist})'".format(tb=self.tb)
			cols = indent('\n     , '.join([c.txtval for c in self.tb.cols]))

		return """{0}
    TO OPERATOR (
         {1}
    )
    SELECT {2}
      FROM OPERATOR (
         {3}
    );""".format(ins, self.cop(), cols, self.pop(None), tb=self.tb)


class TPTJob:
	def __init__(self, name):
		self.name    = name
		self.jobvars = []
		self.steps   = []

	def add(self,o):
		if o == None:
			self.jobvars.append(None)
		elif isinstance(o, tuple):
			self.jobvars.append(TPTVar(o[0],o[1]))
		elif isinstance(o, TPTStep):
			self.steps.append(o)
		elif isinstance(o, list):
			for e in o:
				self.add(e)

	def gen(self, binary=False):
		if [s for s in self.steps if isinstance(s,ApplyDDL)]:
			self.jobvars.append(TPTVar('DDLErrorList', ['3807','3624']))

		jvars = '\n'.join(['' if o == None else str(o) for o in self.jobvars])
		steps = '\n\n'.join([str(o) for o in self.steps])

		return """\
DEFINE JOB {0}
(
    {1}

    {2}
);""".format(self.name, indent(jvars), indent(steps))

	def run(self, jobvar=None, chkpt=None, binary=False):
		import subprocess
		import tempfile

		tmp = tempfile.NamedTemporaryFile()
		tmp.write(self.gen(binary).encode('utf8'))
		tmp.flush()

		cmd = 'tbuild -f {0} '.format(tmp.name)
		if jobvar:
			cmd += '-v {0} '.format(jobvar)
		if chkpt:
			cmd += '-z {0} '.format(chkpt)
		cmd += self.name

		logger.info('TPT Script:\n' + str(self))
		logger.info('Invoking command: ' + cmd)

		try:
			subprocess.check_call(cmd, shell=True)
		except subprocess.CalledProcessError as msg:
			raise Err('tbuild command failed with error code: {0}'.format(msg.returncode))
		finally:
			tmp.close()


def main():
	try:
		user_args()

		if args.limits:
			size_thresholds = args.limits

		tblist = mk_tblist(args)
		job = mk_tptjob(args.job or 'TPTLoad', tblist)

		if args.run:
			job.run(args.jobvar, args.chkp, args.binary)
		else:
			print(job.gen(args.binary))

		return 0

	except Err as msg:
		logger.error(msg)
	except Exception as msg:
		logger.exception(msg)

	return 8


def user_args():
	global args

	import argparse
	import textwrap

	p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description = __doc__, epilog=textwrap.dedent("""\
	Examples:
	  %(prog)s table1 table2 table3
	  %(prog)s --dir /path/to/files/ --src '/$/.tar.gz/'  --db TGTDB --stats --qb 'JOBNAME=MYJOB;' table1 table2 table3
	  %(prog)s --td --src '/^dev_/prd_/'  --stats --trunc-sp PrepTableForLoad dev_db1.table1 dev_db2.table2 dev_db2.table3
	  %(prog)s --odbc ODBCDSN --src '/(.*)/SRCDB..\\1/' --no-trunc --stats table1 table2 table3"""))

	p.add_argument('tbl', nargs='+', help='Table names')

	g = p.add_argument_group('Job options')
	g.add_argument('-j', '--job',    metavar='NAME',             help='Name of the TPT Job')
	g.add_argument('-z', '--chkp',   metavar='INT',              help='Checkpoint interval')
	g.add_argument('-v', '--jobvar', metavar='STR',              help='TPT Job variable file')
	g.add_argument('--qb',           metavar='QB',   default='', help='Additional QUERY_BAND information')
	g.add_argument('--no-trunc', dest='trunc', action='store_false',  help='Assume tables to be empty; do not generate SQL to truncate tables')
	g.add_argument('--trunc-sp',     metavar='SP',               help='Stored-procedure to CALL for truncating table (Default use DELETE statement)')
	g.add_argument('--stats',        action='store_true',        help='Collect stats after load')
	g.add_argument('--run',          action='store_true',        help='Run the resulting TPT script (only on Linux)')

	g = p.add_argument_group('Source options')
	x = g.add_mutually_exclusive_group()
	x.add_argument('--td',           action='store_true',        help='Load data from another Teradata system')
	x.add_argument('--odbc',         metavar='CONN',             help='Load data from ODBC connection')
	g.add_argument('--src', '-f',    metavar='PAT',              help='File/Table name pattern (default: /$/.txt/ for files only)')

	g = p.add_argument_group('Load options')
	g.add_argument('-d', '--db','--database',                    help='Default database name')
	g.add_argument('-e', '--errlim', metavar='INT', default=1, type=int, help='Error limit (default 1)')
	g.add_argument('-w', '--tempdb', metavar='DB',               help='Database namcreating temporary tables')
	g.add_argument('-p', '--pinst',  metavar='INT', type=int,    help='Number of producer instances')
	g.add_argument('-c', '--cinst',  metavar='INT', type=int,    help='Number of consumer instances')

	x = g.add_mutually_exclusive_group()
	x.add_argument('--large',  dest='size', action='store_const', const='LARGE',  help='Use UtilityDataSize=LARGE')
	x.add_argument('--medium', dest='size', action='store_const', const='MEDIUM', help='Use UtilityDataSize=MEDIUM')
	x.add_argument('--small',  dest='size', action='store_const', const='SMALL',  help='Use UtilityDataSize=SMALL')
	x.add_argument('--tiny',   dest='size', action='store_const', const='TINY',   help='Use STREAM operator to load data')

	g = p.add_argument_group('File only options')
	g.add_argument('--dir',    metavar='PATH',      default='',  help='Directory containing input file(s)')
	g.add_argument('--dlm',    metavar='CHAR/INT',  default='\t',help='Field delimiter (default=9 (TAB))')
	g.add_argument('--null',   metavar='CHAR',      default='',  help="NUL value (default='')")
	g.add_argument('--binary', action='store_true',              help='Input data is in Teradata BINARY format')
	g.add_argument('--fit',    action='store_true',              help='Truncate large data values')
	g.add_argument('--escape', metavar='CHAR',      default='\\',help='Escape for Text delimiter (default "\\")')
	g.add_argument('--limits', metavar='INT', default=None, type=float, nargs=3, help='File size thresholds as <tiny> <small> <medium>, for Teradata Utility settings: Default 1e6 1e9 10e9')

	g = p.add_argument_group('Stream only options')
	g.add_argument('-s', '--sess', metavar='INT',   default=10,   type=int, help='Number of sessions for STREAM operator')
	g.add_argument('-k', '--pack', metavar='INT',   default=None, type=int, help='Pack factor for STREAM operator')

	p.add_argument('-V', '--verbose', default=0, action='count', help='print verbose log information. Use -VV for more details')

	args = p.parse_args()

	if   args.verbose > 1: logger.setLevel(logging.DEBUG)
	elif args.verbose > 0: logger.setLevel(logging.INFO)

	return args


def mk_tblist(args):
	if args.src:
		import re

		dlm, pat = args.src[0], args.src[1:]
		if pat[-1] == dlm:
			pat = pat[:-1]
		try:
			pat, repl = pat.split(dlm)
		except:
			raise Err('Invalid pattern for --src|-f parameter')
		Target.tgt2src = lambda t: re.sub(pat,repl,t, re.I)

	elif  not (args.odbc or args.td):
		import os.path as p
		Target.tgt2src = lambda t: p.join(args.dir,t+'.txt')

	Tgt = DBTarget if args.odbc or args.td else FileTarget

	if len(args.tbl) == 1:
		return [Tgt(args.tbl[0], size=args.size, tempdb=args.tempdb)]
	else:
		return [Tgt(t, seq=e, size=args.size, tempdb=args.tempdb) for e, t in enumerate(args.tbl, start=1)]


def mk_tptjob(jobname, tblist):
	job = TPTJob(jobname)

	if args.db: job.add( ('TargetWorkingDatabase', args.db) )
	if args.tempdb: job.add( ('UtilDatabase', args.tempdb) )

	job.add(None)
	if args.td:
		job.add(('ExportDateForm', 'AnsiDate'))
	elif args.odbc:
		job.add([ ('ODBCConnectString','DSN={0}'.format(args.odbc)), ('ODBCTruncateData','Yes') ]);
	else:
		job.add( ('DCPOpenMode','Read') )
		if args.dir: job.add(('DCPDirectoryPath', args.dir))
		if args.binary:
			job.add([('DCPFormat','Binary'), ('DCPIndicatorMode','Yes')])
		else:
			job.add( ('DCPFormat','Delimited') )
			try:
				job.add( ('DCPTextDelimiterHEX', hex(int(args.dlm))[2:]) )
			except ValueError:
				job.add( ('DCPTextDelimiter', args.dlm) )
			job.add( ('DCPEscapeTextDelimiter', args.escape) )
			job.add( ('DCPNullColumns','Yes' if args.null == '' else 'N') )
		if args.fit: job.add( ('DCPTruncateColumnData', 'Yes') )

	job.add(None)
	job.add( ('LoadErrorLimit', args.errlim) )
	if args.pinst:  job.add( ('PInstances',args.pinst) )
	if args.cinst:  job.add( ('CInstances',args.cinst) )

	need_stream = len([t for t in tblist if t.size == 'TINY']) > 0
	if need_stream:
		job.add(None)
		job.add( [('StreamMaxSessions', args.sess), ('StreamErrorLimit', args.errlim)] )
		if args.pack:
			job.add( ('StreamPack', args.pack) )

	if args.trunc:
		sql = "'DELETE FROM {tb.name}'" if not args.trunc_sp else "'CALL "+ args.trunc_sp + "('''{tb.name}''')'"
		job.add( ApplyDDL('TruncTbl', [sql.format(tb=tb) for tb in tblist]) )

	for tb in tblist:
		job.add(ApplyLoad(tb))

	if args.stats:
		job.add( ApplyDDL('CollStats', ["'COLLECT STATS ON {tb.name}'".format(tb=tb) for tb in tblist]) )

	return job


if __name__ == '__main__':
	import sys
	sys.exit(main())
