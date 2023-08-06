from glob import glob
import os
import sys

from setuptools import setup, Extension
from distutils.version import LooseVersion
from distutils.command.sdist import sdist as _sdist
from distutils.command.build_ext import build_ext as _build_ext

import versioneer

MIN_CYTHON_VERSION = '0.17'

if sys.version_info < (3, 4):
	sys.stdout.write("At least Python 3.4 is required.\n")
	sys.exit(1)


def no_cythonize(extensions, **_ignore):
	"""
	Change file extensions from .pyx to .c or .cpp.

	Copied from Cython documentation
	"""
	for extension in extensions:
		sources = []
		for sfile in extension.sources:
			path, ext = os.path.splitext(sfile)
			if ext in ('.pyx', '.py'):
				if extension.language == 'c++':
					ext = '.cpp'
				else:
					ext = '.c'
				sfile = path + ext
			sources.append(sfile)
		extension.sources[:] = sources


def check_cython_version():
	"""exit if Cython not found or out of date"""
	try:
		from Cython import __version__ as cyversion
	except ImportError:
		sys.stdout.write(
			"ERROR: Cython is not installed. Install at least Cython version " +
			str(MIN_CYTHON_VERSION) + " to continue.\n")
		sys.exit(1)
	if LooseVersion(cyversion) < LooseVersion(MIN_CYTHON_VERSION):
		sys.stdout.write(
			"ERROR: Your Cython is at version '" + str(cyversion) +
			"', but at least version " + str(MIN_CYTHON_VERSION) + " is required.\n")
		sys.exit(1)


cmdclass = versioneer.get_cmdclass()
versioneer_build_ext = cmdclass.get('build_ext', _build_ext)
versioneer_sdist = cmdclass.get('sdist', _sdist)


class build_ext(versioneer_build_ext):
	def run(self):
		# If we encounter a PKG-INFO file, then this is likely a .tar.gz/.zip
		# file retrieved from PyPI that already includes the pre-cythonized
		# extension modules, and then we do not need to run cythonize().
		if os.path.exists('PKG-INFO'):
			no_cythonize(extensions)
		else:
			# Otherwise, this is a 'developer copy' of the code, and then the
			# only sensible thing is to require Cython to be installed.
			check_cython_version()
			from Cython.Build import cythonize
			self.extensions = cythonize(self.extensions)
		versioneer_build_ext.run(self)


class sdist(versioneer_sdist):
	def run(self):
		# Make sure the compiled Cython files in the distribution are up-to-date
		from Cython.Build import cythonize
		check_cython_version()
		cythonize(extensions)
		versioneer_sdist.run(self)


cmdclass['build_ext'] = build_ext
cmdclass['sdist'] = sdist

extensions = [
	Extension('sqt._helpers', sources=['sqt/_helpers.pyx']),
]


setup(
	name = 'sqt',
	version = versioneer.get_version(),
	author = 'Marcel Martin',
	author_email = 'marcel.martin@scilifelab.se',
	url = 'https://bitbucket.org/marcelm/sqt',
	description = 'Command-line tools for the analysis of high-throughput sequencing data',
	license = 'MIT',
	cmdclass = cmdclass,
	packages = [ 'sqt', 'sqt.io', 'sqt.commands' ],
	entry_points = {'console_scripts': [
		'sqt = sqt.__main__:main',
		#'sqt-addadapt = sqt.commands.addadapt:main',
		#'sqt-bam2fastq = sqt.commands.bam2fastq:main',
		#'sqt-bamstats = sqt.commands.bamstats:main',
		#'sqt-checkfastqpe = sqt.commands.checkfastqpe:main',
		#'sqt-checkvcfref = sqt.commands.checkvcfref:main',
		#'sqt-compare-sequences = sqt.commands.compare_sequences:main',
		#'sqt-coverage = sqt.commands.coverage:main',
		#'sqt-fastaextract = sqt.commands.fastaextract:main',
		#'sqt-fastamutate = sqt.commands.fastamutate:main',
		#'sqt-fastastats = sqt.commands.fastastats:main',
		#'sqt-fastxmod = sqt.commands.fastxmod:main',
		#'sqt-fixbam64 = sqt.commands.fixbam64:main',
		#'sqt-globalalign = sqt.commands.globalalign:main',
		#'sqt-histogram = sqt.commands.histogram:main',
		#'sqt-qualityguess = sqt.commands.qualityguess:main',
		#'sqt-readcov = sqt.commands.readcov:main',
		#'sqt-samfixn = sqt.commands.samfixn:main',
		#'sqt-simreads = sqt.commands.simreads:main',
		#'sqt-translate = sqt.commands.translate:main',
	]},
	install_requires = [
		'pysam!=0.9.0',
		'cutadapt',
		'matplotlib',
		'seaborn',
		'xopen',
	],
	ext_modules = extensions,
	test_suite = 'nose.collector',
	classifiers = [
		"Development Status :: 4 - Beta",
		#Development Status :: 5 - Production/Stable
		"Environment :: Console",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Bio-Informatics"
	]
)
