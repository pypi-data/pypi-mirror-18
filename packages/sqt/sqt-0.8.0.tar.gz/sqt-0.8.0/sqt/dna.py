#!/usr/bin/env python3
"""
- Python 2 and 3 compatible fast reverse complement
- definition of genetic code (triplets to amino acids)
- fast translation of nucleotide strings to amino acids
- other misc. functions
"""
import sys
import re
import random
from ._codons import GENETIC_CODE  # for re-export
from sqt._helpers import nt_to_aa


if sys.version < '3':
	from string import maketrans
else:
	maketrans = bytes.maketrans
	_TR_STR = str.maketrans('ACGTUMRWSYKVHDBNacgtumrwsykvhdbn', 'TGCAAKYWSRMBDHVNtgcaakywsrmbdhvn')

_TR = maketrans(b'ACGTUMRWSYKVHDBNacgtumrwsykvhdbn', b'TGCAAKYWSRMBDHVNtgcaakywsrmbdhvn')

if sys.version < '3':
	def reverse_complement(s):
		return s.translate(_TR)[::-1]
else:
	def reverse_complement(s):
		if isinstance(s, str):
			return s.translate(_TR_STR)[::-1]
		else:
			return s.translate(_TR)[::-1]


AMINO_ACID_REGEXES = dict(
	A='GC[ACGT]',
	C='TG[CT]',
	D='GA[CT]',
	E='GA[AG]',
	F='TT[CT]',
	G='GG[ACGT]',
	H='CA[CT]',
	I='AT[ACT]',
	K='AA[AG]',
	L='(CT[ACGT]|TT[AG])',
	M='ATG',
	N='AA[CT]',
	P='CC[ACGT]',
	Q='CA[AG]',
	R='(AG[AG]|CG[ACGT])',
	S='AG[CT]|TC[ACGT]',
	T='AC[ACGT]',
	V='GT[ACGT]',
	W='TGG',
	Y='TA[CT]',
	X='[ACGT][ACGT][ACGT]'
)


def amino_acid_regex(aa_sequence, compile=False):
	"""
	Given an amino acid sequence, return a regular expression that can be used
	to match a nucleotide sequence. If compile is True, the regular expression
	is compiled with re.compile, otherwise the regex is returned as a string.
	"""
	regex = ''.join(AMINO_ACID_REGEXES[aa] for aa in aa_sequence)
	return re.compile(regex) if compile else regex


def n_intervals(sequence, N='N'):
	"""
	Given a sequence, yield all intervals containing only N characters as
	tuples (start, stop). If the sequence is a bytes/bytearray object,
	set N=ord(b'N')

	>>> list(n_intervals('ACGTnNAC'))
	[(4, 6)]
	>>> list(n_intervals(b'ACGTnNAC', N=ord(b'N')))
	[(4, 6)]
	"""
	sequence = sequence.upper()
	start = sequence.find(N)
	while start >= 0:
		stop = start + 1
		while stop < len(sequence) and sequence[stop] == N:
			stop += 1
		yield (start, stop)
		start = sequence.find(N, stop)


def intervals_complement(intervals, length):
	"""
	Given an iterable of sorted, nonoverlapping intervals as (start, stop)
	pairs, yield the complementary intervals. The result is equivalent to
	[(0, length)] minus the given intervals.

	>>> list(intervals_complement([(1, 2), (4, 6)], length=10))
	[(0, 1), (2, 4), (6, 10)]
	"""
	prev_stop = 0
	for start, stop in intervals:
		if start >= length:
			break
		if prev_stop != start:
			yield (prev_stop, start)
		prev_stop = stop
	if prev_stop < length:
		yield (prev_stop, length)


def mutate(seq, substitution_rate=0.1, indel_rate=0.01, alphabet='ACGT', counts=False):
	"""
	Mutate a DNA sequence by randomly introducing substitutions and indels.
	This does not use a very sophisticated model.

	Return the mutated sequence.

	substitution_rate -- The probability at which an individual base is substituted with a different one.

	indel_rate -- At any position, a random base is inserted at probability indel_rate/2, and
		the base is deleted at probability indel_rate/2.


	counts -- If this is True, a triple (mutated_sequence, number_of_substitutions, number_of_indels)
		is returned instead of just the sequence.
	"""
	other_chars = {}
	for c in alphabet:
		other_chars[c] = alphabet.replace(c, '')
	mutated = []
	n_sub = 0
	n_indel = 0
	indels = indel_rate > 0
	for c in seq:
		c = c.upper()
		r = random.random()
		if r < substitution_rate:
			# mutate base
			d = random.choice(other_chars.get(c, alphabet))
			mutated.append(d)
			n_sub += 1
		elif indels and r < (substitution_rate + 0.5 * indel_rate):
			# insertion
			mutated.append(random.choice(alphabet))
			mutated.append(c)
			n_indel += 1
		elif indels and r < (substitution_rate + indel_rate):
			n_indel += 1
			# deletion
			pass
		else:
			# no change
			mutated.append(c)
	if counts:
		return ''.join(mutated), n_sub, n_indel
	else:
		return ''.join(mutated)
