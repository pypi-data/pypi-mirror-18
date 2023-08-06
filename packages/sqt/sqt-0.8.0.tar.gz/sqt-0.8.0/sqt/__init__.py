from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .args import HelpfulArgumentParser
from .io.fasta import (
	SequenceReader, FastaReader, FastqReader, FastaWriter, FastqWriter,
	IndexedFasta, guess_quality_base )
from .io.gtf import GtfReader
from .cigar import Cigar

# TODO Deprecated
from xopen import xopen
