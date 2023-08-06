#!/usr/bin/env python3
"""
"""
import sys
from collections import Counter
from sqt import SequenceReader, HelpfulArgumentParser

# Make potential import failures happen before we read in files
import matplotlib as mpl
mpl.use('Agg')  # enable matplotlib over an ssh connection without X
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings

__author__ = "Marcel Martin"

warnings.filterwarnings('ignore', 'axes.color_cycle is deprecated and replaced with axes.prop_cycle')

def add_arguments(parser):
	arg = parser.add_argument
	arg('--zero', default=False, action='store_true', help='Print also rows with a count of zero')

	arg('--plot', default=None, help='Plot to this file (.pdf or .png). '
		'If multiple sequence files given, plot only total.')
	arg('--bins', default=50, type=int, help='Number of bins in the plot. '
		'Default: %(default)s')
	arg('--maxy', default=None, type=float, help='Maximum y in plot')
	arg('--left', default=0, type=float, help='Minimum x in plot')
	arg('--outliers', default=False, action='store_true',
		help='In the plot, summarize outliers greater than the 99.9 percentile '
		'in a red bar.')
	arg('--title', default='Read length histogram of {}',
		help="Plot title. {} is replaced with the input file name. "
		"Default: '%(default)s'")

	arg('seqfiles', nargs='+', metavar='FASTA/FASTQ',
		help='Input FASTA/FASTQ file(s) (may be gzipped).')


def length_histogram(path):
	"""Return a list of lengths """
	lengths = []
	with SequenceReader(path) as reader:
		for record in reader:
			lengths.append(len(record.sequence))
	return lengths


def plot_histogram(lengths, path, title, max_y=None, min_x=0, bins=50, outliers=False):
	"""
	Plot histogram of lengths to path

	If outliers is True, then the lengths greater than the 99.9 percentile are
	marked separately with bar colored in red.
	"""
	lengths = np.array(lengths)
	if outliers:
		histomax = int(np.percentile(lengths, 99.9) * 1.01)
	else:
		histomax = int(max(lengths))
	larger = sum(lengths > histomax)

	fig = plt.figure(figsize=(20/2.54, 10/2.54))
	ax = fig.gca()
	ax.set_xlabel('Read length')
	ax.set_ylabel('Frequency')
	ax.set_title(title)
	_, borders, _ = ax.hist(lengths, bins=bins, range=(min_x, histomax))
	if outliers:
		w = borders[1] - borders[0]
		ax.bar([histomax], [larger], width=w, color='red')
		ax.set_xlim(min_x, histomax + 1.5 * w)
	if max_y is not None:
		ax.set_ylim(0, max_y)
	fig.set_tight_layout(True)
	fig.savefig(path)


def main(args=None):
	if args is None:
		parser = HelpfulArgumentParser(description=__doc__)
		add_arguments(parser)
		args = parser.parse_args()


if __name__ == '__main__':
	main()
