#! /usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
import gitime.database as db

class DbSetupInstall(install):

	def run(self):
		install.run(self)
		db.first_time_setup()


setup(
	name="gitime",
	version="1.0a",
	description="build an invoice with your tasks and hours worked from your commit messages",
	author="Jonathan Goodnow",
	author_email="goodnow.jonathan@gmail.com",
	url="https://github.com/jongoodnow/gitime",
	keywords=['git', 'invoice', 'timer'],
	license="MIT",
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Topic :: Utilities'
	],
	entry_points={
		'console_scripts': [
			'gitime = gitime:main'
		]
	},
	cmdclass={
		'install': DbSetupInstall
	}
)