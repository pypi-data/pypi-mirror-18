from setuptools import setup

with open("README.rst", encoding="utf-8") as f:
	readme = f.read()

setup(
	name='tdtools',
	description='A Collection of assorted Teradata Tools',
	long_description=readme,
	url='https://bitbucket.org/padhia/tdtools',

	author='Paresh Adhia',
	version='0.4.0',
	license='GPL',

	packages=['tdtools','tdtools.show','tdtools.ls'],
	package_data={'tdtools':['*.json']},
	install_requires=['teradata'],

	keywords='teradata teradata_15.10',

	entry_points={
		'console_scripts': [
			'lstvm=tdtools.ls.tvm:main',
			'lstb=tdtools.ls.tvm:main',
			'lspr=tdtools.ls.tvm:main',
			'lsvw=tdtools.ls.tvm:main',
			'lsji=tdtools.ls.tvm:main',
			'dbtree=tdtools.dbtree:main',
			'vwtree=tdtools.vwtree:main',
			'tptload=tdtools.tptload:main',
			'showdb=tdtools.show.db:main',
			'showgrant=tdtools.show.grant:main',
			'showprof=tdtools.show.prof:main',
			'showrole=tdtools.show.role:main',
			'showtvm=tdtools.show.tvm:main',
			'showzone=tdtools.show.zone:main',
		],
	},

	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Intended Audience :: End Users/Desktop',

		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: POSIX :: Linux',

		'Topic :: Database',
		'Topic :: Software Development',
		'Topic :: Utilities',

		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
	],
)
