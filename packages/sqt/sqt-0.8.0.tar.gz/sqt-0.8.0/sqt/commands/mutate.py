#!/usr/bin/env python3
"""
Mutate nucleotides in a FASTA or FASTQ file

The modified sequences are written to standard output.
"""
import sys
import random
from sqt import HelpfulArgumentParser
from sqt.io.fasta import FastaReader, FastaWriter
from sqt.dna import mutate

__author__ = "Marcel Martin"


def main():
	parser = HelpfulArgumentParser(description=__doc__)
	parser.add_argument("--rate", type=float, default=0.03,
		help="Substitution rate (default: %(default)s)")
	parser.add_argument("--indel-rate", type=float, default=0.0005,
		help="Indel rate (default: %(default)s)")
	parser.add_argument("--seed", type=int, default=None,
		help="Set random seed for reproducible runs (default: use different seed each run)")
	parser.add_argument("fasta", metavar='FASTA-file', help="Input FASTA file")
	args = parser.parse_args()

	if args.seed is not None:
		random.seed(args.seed)
	fasta_output = FastaWriter(sys.stdout, line_length=80)
	for record in FastaReader(args.fasta):
		mutated, n_sub, n_indel = mutate(record.sequence, rate=args.rate, alphabet='ACGT', indel_rate=args.indel_rate, counts=True)
		fasta_output.write(record.name + '-sub{}-indel{}'.format(n_sub, n_indel), mutated)


if __name__ == '__main__':
	main()
