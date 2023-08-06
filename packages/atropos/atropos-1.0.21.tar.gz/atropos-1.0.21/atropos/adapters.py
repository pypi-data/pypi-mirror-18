# coding: utf-8
"""
Adapters
"""
from collections import defaultdict
import logging
import os
import pickle
import re
import sys
from urllib.request import urlopen
from atropos import align, colorspace
from atropos.align import Match
from atropos.seqio import ColorspaceSequence, FastaReader

# Constants for the find_best_alignment function.
# The function is called with SEQ1 as the adapter, SEQ2 as the read.
# TODO get rid of those constants, use strings instead
BACK = align.START_WITHIN_SEQ2 | align.STOP_WITHIN_SEQ2 | align.STOP_WITHIN_SEQ1
FRONT = align.START_WITHIN_SEQ2 | align.STOP_WITHIN_SEQ2 | align.START_WITHIN_SEQ1
PREFIX = align.STOP_WITHIN_SEQ2
SUFFIX = align.START_WITHIN_SEQ2
ANYWHERE = align.SEMIGLOBAL
LINKED = 'linked'

def parse_braces(sequence):
    """
    Replace all occurrences of ``x{n}`` (where x is any character) with n
    occurrences of x. Raise ValueError if the expression cannot be parsed.

    >>> parse_braces('TGA{5}CT')
    TGAAAAACT
    """
    # Simple DFA with four states, encoded in prev
    result = ''
    prev = None
    for s in re.split('(\{|\})', sequence):
        if s == '':
            continue
        if prev is None:
            if s == '{':
                raise ValueError('"{" must be used after a character')
            if s == '}':
                raise ValueError('"}" cannot be used here')
            prev = s
            result += s
        elif prev == '{':
            prev = int(s)
            if not 0 <= prev <= 10000:
                raise ValueError('Value {} invalid'.format(prev))
        elif isinstance(prev, int):
            if s != '}':
                raise ValueError('"}" expected')
            result = result[:-1] + result[-1] * prev
            prev = None
        else:
            if s != '{':
                raise ValueError('Expected "{"')
            prev = '{'
    # Check if we are in a non-terminating state
    if isinstance(prev, int) or prev == '{':
        raise ValueError("Unterminated expression")
    return result

ADAPTER_TYPES = dict(back=BACK, front=FRONT, anywhere=ANYWHERE)

class AdapterParser(object):
    """
    Factory for Adapter classes that all use the same parameters (error rate,
    indels etc.). The given **kwargs will be passed to the Adapter constructors.
    """
    def __init__(self, colorspace=False, cache=None, **kwargs):
        self.colorspace = colorspace
        self.cache = cache
        self.constructor_args = kwargs
        self.adapter_class = ColorspaceAdapter if colorspace else Adapter

    def parse(self, spec=None, name=None, cmdline_type='back'):
        """
        Parse an adapter specification not using ``file:`` notation and return
        an object of an appropriate Adapter class. The notation for anchored
        5' and 3' adapters is supported. If the name parameter is None, then
        an attempt is made to extract the name from the specification
        (If spec is 'name=ADAPTER', name will be 'name'.)

        cmdline_type -- describes which commandline parameter was used (``-a``
        is 'back', ``-b`` is 'anywhere', and ``-g`` is 'front').
        """
        if cmdline_type not in ADAPTER_TYPES:
            raise ValueError('cmdline_type cannot be {0!r}'.format(cmdline_type))
        where = ADAPTER_TYPES[cmdline_type]
        
        if name is None and spec is None:
            raise ValueError("Either name or spec must be given")
        elif name is None:
            if self.cache and self.cache.has_name(spec):
                name = spec
                spec = self.cache.get_for_name(name)
        elif spec is None:
            if self.cache and self.cache.has_name(name):
                spec = self.cache.get_for_name(name)
        
        if spec is None:
            raise ValueError("Name not found: {}".format(name))
        elif name is None:
            name, spec = self._extract_name(spec)
        
        if self.cache and name is not None:
            self.cache.add(name, spec)
            
        sequence = spec
        if where == FRONT and spec.startswith('^'):  # -g ^ADAPTER
            sequence, where = spec[1:], PREFIX
        elif where == BACK:
            sequence1, middle, sequence2 = spec.partition('...')
            if middle == '...':
                if not sequence1:  # -a ...ADAPTER
                    sequence = sequence1[3:]
                elif not sequence2:  # -a ADAPTER...
                    sequence, where = spec[:-3], PREFIX
                else:  # -a ADAPTER1...ADAPTER2
                    if self.colorspace:
                        raise NotImplementedError('Using linked adapters in colorspace is not supported')
                    if sequence1.startswith('^') or sequence2.endswith('$'):
                        raise NotImplementedError('Using "$" or "^" when '
                            'specifying a linked adapter is not supported')
                    return LinkedAdapter(sequence1, sequence2, name=name,
                        **self.constructor_args)
            elif spec.endswith('$'):   # -a ADAPTER$
                sequence, where = spec[:-1], SUFFIX
        
        if not sequence:
            raise ValueError("The adapter sequence is empty.")
        
        return self.adapter_class(sequence, where, name=name, **self.constructor_args)
    
    def parse_multi(self, back=[], anywhere=[], front=[]):
        """
        Parse all three types of commandline options that can be used to
        specify adapters. back, anywhere and front are lists of strings,
        corresponding to the respective commandline types (-a, -b, -g).

        Return a list of appropriate Adapter classes.
        """
        adapters = []
        for specs, cmdline_type in (back, 'back'), (anywhere, 'anywhere'), (front, 'front'):
            for spec in specs:
                if spec.startswith('file:'):
                    # read adapter sequences from a file
                    with FastaReader(spec[5:]) as fasta:
                        for record in fasta:
                            name = record.name.split(None, 1)[0]
                            adapters.append(self.parse(record.sequence, name, cmdline_type))
                else:
                    adapters.append(self.parse(spec=spec, cmdline_type=cmdline_type))
        return adapters
    
    def _extract_name(self, spec):
        """
        Parse an adapter specification given as 'name=adapt' into 'name' and 'adapt'.
        """
        fields = spec.split('=', 1)
        if len(fields) > 1:
            name, spec = fields
            name = name.strip()
        else:
            name = None
        spec = spec.strip()
        return name, spec

def _generate_adapter_name(_start=[1]):
    name = str(_start[0])
    _start[0] += 1
    return name

class Adapter(object):
    """
    An adapter knows how to match itself to a read.
    In particular, it knows where it should be within the read and how to interpret
    wildcard characters.

    where --  One of the BACK, FRONT, PREFIX, SUFFIX or ANYWHERE constants.
        This influences where the adapter is allowed to appear within in the
        read and also which part of the read is removed.

    sequence -- The adapter sequence as string. Will be converted to uppercase.
        Also, Us will be converted to Ts.

    max_error_rate -- Maximum allowed error rate. The error rate is
        the number of errors in the alignment divided by the length
        of the part of the alignment that matches the adapter.

    minimum_overlap -- Minimum length of the part of the alignment
        that matches the adapter.

    read_wildcards -- Whether IUPAC wildcards in the read are allowed.

    adapter_wildcards -- Whether IUPAC wildcards in the adapter are
        allowed.

    name -- optional name of the adapter. If not provided, the name is set to a
        unique number.
    """
    def __init__(self, sequence, where, max_error_rate=0.1, min_overlap=3,
                 read_wildcards=False, adapter_wildcards=True, name=None, indels=True,
                 indel_cost=1, match_probability=None, max_rmp=None):
        self.debug = False
        self.name = _generate_adapter_name() if name is None else name
        self.sequence = parse_braces(sequence.upper().replace('U', 'T'))
        assert len(self.sequence) > 0
        self.where = where
        self.max_error_rate = max_error_rate
        self.min_overlap = min(min_overlap, len(self.sequence))
        self.match_probability = None
        if match_probability and max_rmp is not None:
            self.match_probability = match_probability
            self.max_rmp = max_rmp
        self.indels = indels
        self.adapter_wildcards = adapter_wildcards and not set(self.sequence) <= set('ACGT')
        self.read_wildcards = read_wildcards
        # redirect trimmed() to appropriate function depending on adapter type
        trimmers = {
            FRONT: self._trimmed_front,
            PREFIX: self._trimmed_front,
            BACK: self._trimmed_back,
            SUFFIX: self._trimmed_back,
            ANYWHERE: self._trimmed_anywhere
        }
        self.trimmed = trimmers[where]
        if where == ANYWHERE:
            self._front_flag = None  # means: guess
        else:
            self._front_flag = where not in (BACK, SUFFIX)
        # statistics about length of removed sequences
        self.lengths_front = defaultdict(int)
        self.lengths_back = defaultdict(int)
        self.errors_front = defaultdict(lambda: defaultdict(int))
        self.errors_back = defaultdict(lambda: defaultdict(int))
        self.adjacent_bases = { 'A': 0, 'C': 0, 'G': 0, 'T': 0, '': 0 }

        self.aligner = align.Aligner(self.sequence, self.max_error_rate,
            flags=self.where, wildcard_ref=self.adapter_wildcards, wildcard_query=self.read_wildcards)
        self.aligner.min_overlap = self.min_overlap
        if self.indels:
            self.aligner.indel_cost = indel_cost
        else:
            # TODO
            # When indels are disallowed, an entirely different algorithm
            # should be used.
            self.aligner.indel_cost = 100000

    def __repr__(self):
        return '<Adapter(name="{name}", sequence="{sequence}", where={where}, '\
            'max_error_rate={max_error_rate}, min_overlap={min_overlap}, '\
            'read_wildcards={read_wildcards}, '\
            'adapter_wildcards={adapter_wildcards}, '\
            'indels={indels})>'.format(**vars(self))

    def enable_debug(self):
        """
        Print out the dynamic programming matrix after matching a read to an
        adapter.
        """
        self.debug = True
        self.aligner.enable_debug()
    
    def match_to(self, read):
        """
        Attempt to match this adapter to the given read.

        Return an Match instance if a match was found;
        return None if no match was found given the matching criteria (minimum
        overlap length, maximum error rate).
        """
        read_seq = read.sequence.upper()
        
        # try to find an exact match first unless wildcards are allowed
        pos = -1
        if not self.adapter_wildcards:
            if self.where == PREFIX:
                pos = 0 if read_seq.startswith(self.sequence) else -1
            elif self.where == SUFFIX:
                pos = (len(read_seq) - len(self.sequence)) if read_seq.endswith(self.sequence) else -1
            else:
                pos = read_seq.find(self.sequence)
        
        if pos >= 0:
            l = len(self.sequence)
            return Match(0, l, pos, pos + l, l, 0, self._front_flag, self, read)
        
        # try approximate matching
        alignment = None
        if not self.indels and self.where in (PREFIX, SUFFIX):
            if self.where == PREFIX:
                alignment = align.compare_prefixes(self.sequence, read_seq,
                    wildcard_ref=self.adapter_wildcards, wildcard_query=self.read_wildcards)
            else:
                alignment = align.compare_suffixes(self.sequence, read_seq,
                    wildcard_ref=self.adapter_wildcards, wildcard_query=self.read_wildcards)
        else:
            alignment = self.aligner.locate(read_seq)
            if self.debug:
                print(self.aligner.dpmatrix)  # pragma: no cover
        
        if alignment:
            astart, astop, rstart, rstop, matches, errors = alignment
            size = astop - astart
            if (size >= self.min_overlap and errors / size <= self.max_error_rate and (
                    self.match_probability is None or
                    self.match_probability(matches, size) <= self.max_rmp)):
                return Match(
                    astart, astop, rstart, rstop, matches, errors,
                    self._front_flag, self, read)
        
        return None

    def _trimmed_anywhere(self, match):
        """Return a trimmed read"""
        if match.front:
            return self._trimmed_front(match)
        else:
            return self._trimmed_back(match)

    def _trimmed_front(self, match):
        """Return a trimmed read"""
        # TODO move away
        self.lengths_front[match.rstop] += 1
        self.errors_front[match.rstop][match.errors] += 1
        return match.read[match.rstop:]

    def _trimmed_back(self, match):
        """Return a trimmed read without the 3' (back) adapter"""
        # TODO move away
        self.lengths_back[len(match.read) - match.rstart] += 1
        self.errors_back[len(match.read) - match.rstart][match.errors] += 1
        adjacent_base = match.read.sequence[match.rstart-1:match.rstart]
        if adjacent_base not in 'ACGT':
            adjacent_base = ''
        self.adjacent_bases[adjacent_base] += 1
        return match.read[:match.rstart]

    def __len__(self):
        return len(self.sequence)

class ColorspaceAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        super(ColorspaceAdapter, self).__init__(*args, **kwargs)
        has_nucleotide_seq = False
        if set(self.sequence) <= set('ACGT'):
            # adapter was given in basespace
            self.nucleotide_sequence = self.sequence
            has_nucleotide_seq = True
            self.sequence = colorspace.encode(self.sequence)[1:]
        if self.where in (PREFIX, FRONT) and not has_nucleotide_seq:
            raise ValueError("A 5' colorspace adapter needs to be given in nucleotide space")
        self.aligner.reference = self.sequence

    def match_to(self, read):
        """Return Match instance"""
        if self.where != PREFIX:
            return super(ColorspaceAdapter, self).match_to(read)
        # create artificial adapter that includes a first color that encodes the
        # transition from primer base into adapter
        asequence = colorspace.ENCODE[read.primer + self.nucleotide_sequence[0:1]] + self.sequence

        pos = 0 if read.sequence.startswith(asequence) else -1
        if pos >= 0:
            match = Match(
                0, len(asequence), pos, pos + len(asequence),
                len(asequence), 0, self._front_flag, self, read)
        else:
            # try approximate matching
            self.aligner.reference = asequence
            alignment = self.aligner.locate(read.sequence)
            if self.debug:
                print(self.aligner.dpmatrix)  # pragma: no cover
            if alignment is not None:
                match = Match(*(alignment + (self._front_flag, self, read)))
            else:
                match = None

        if match is None:
            return None
        assert match.length > 0 and match.errors / match.length <= self.max_error_rate
        assert match.length >= self.min_overlap
        return match

    def _trimmed_front(self, match):
        """Return a trimmed read"""
        read = match.read
        self.lengths_front[match.rstop] += 1
        self.errors_front[match.rstop][match.errors] += 1
        # to remove a front adapter, we need to re-encode the first color following the adapter match
        color_after_adapter = read.sequence[match.rstop:match.rstop + 1]
        if not color_after_adapter:
            # the read is empty
            return read[match.rstop:]
        base_after_adapter = colorspace.DECODE[self.nucleotide_sequence[-1:] + color_after_adapter]
        new_first_color = colorspace.ENCODE[read.primer + base_after_adapter]
        new_read = read[:]
        new_read.sequence = new_first_color + read.sequence[(match.rstop + 1):]
        new_read.qualities = read.qualities[match.rstop:] if read.qualities else None
        return new_read

    def _trimmed_back(self, match):
        """Return a trimmed read"""
        # trim one more color if long enough
        adjusted_rstart = max(match.rstart - 1, 0)
        self.lengths_back[len(match.read) - adjusted_rstart] += 1
        self.errors_back[len(match.read) - adjusted_rstart][match.errors] += 1
        return match.read[:adjusted_rstart]

    def __repr__(self):
        return '<ColorspaceAdapter(sequence={0!r}, where={1})>'.format(self.sequence, self.where)

class LinkedMatch(object):
    """
    Represent a match of a LinkedAdapter.

    TODO
    It shouldn’t be necessary to have both a Match and a LinkedMatch class.
    """
    def __init__(self, front_match, back_match, adapter):
        self.front_match = front_match
        self.back_match = back_match
        self.adapter = adapter
        assert front_match is not None
    
    def get_info_record(self):
        return self.back_match.get_info_record() if self.back_match else self.front_match.get_info_record()

class LinkedAdapter(object):
    """
    """
    def __init__(self, front_sequence, back_sequence,
            front_anchored=True, back_anchored=False, name=None, **kwargs):
        """
        kwargs are passed on to individual Adapter constructors
        """
        assert front_anchored and not back_anchored
        where1 = PREFIX if front_anchored else FRONT
        where2 = SUFFIX if back_anchored else BACK
        self.front_anchored = front_anchored
        self.back_anchored = back_anchored

        # The following attributes are needed for the report
        self.where = LINKED
        self.name = _generate_adapter_name() if name is None else name
        self.front_adapter = Adapter(front_sequence, where=where1, name=None, **kwargs)
        self.back_adapter = Adapter(back_sequence, where=where2, name=None, **kwargs)

    def enable_debug(self):
        self.front_adapter.enable_debug()
        self.back_adapter.enable_debug()

    def match_to(self, read):
        """
        Match the linked adapters against the given read. If the 'front' adapter
        is not found, the 'back' adapter is not searched for.
        """
        front_match = self.front_adapter.match_to(read)
        if front_match is None:
            return None
        # TODO use match.trimmed() instead as soon as that does not update
        # statistics anymore
        read = read[front_match.rstop:]
        back_match = self.back_adapter.match_to(read)
        return LinkedMatch(front_match, back_match, self)

    def trimmed(self, match):
        front_trimmed = self.front_adapter.trimmed(match.front_match)
        if match.back_match:
            return self.back_adapter.trimmed(match.back_match)
        else:
            return front_trimmed

    # Lots of forwarders (needed for the report). I’m sure this can be done
    # in a better way.

    @property
    def lengths_front(self):
        return self.front_adapter.lengths_front

    @property
    def lengths_back(self):
        return self.back_adapter.lengths_back

    @property
    def errors_front(self):
        return self.front_adapter.errors_front

    @property
    def errors_back(self):
        return self.back_adapter.errors_back

    @property
    def adjacent_bases(self):
        return self.back_adapter.adjacent_bases

class AdapterCache(object):
    def __init__(self, path=".adapters", auto_reverse_complement=False):
        self.path = path
        self.auto_reverse_complement = auto_reverse_complement
        if path and os.path.exists(path):
            with open(path, "rb") as cache:
                (self.seq_to_name, self.name_to_seq) = pickle.load(cache)
        else:
            self.seq_to_name = {}
            self.name_to_seq = {}
    
    @property
    def empty(self):
        return len(self.seq_to_name) == 0
    
    def save(self):
        if self.path is not None:
            with open(self.path, "wb") as cache:
                pickle.dump((self.seq_to_name, self.name_to_seq), cache)
    
    def add(self, name, seq):
        self._add(name, seq)
        if self.auto_reverse_complement:
            self._add("{}_rc".format(name), reverse_complement(seq))
    
    def _add(self, name, seq):
        if seq not in self.seq_to_name:
            self.seq_to_name[seq] = set()
        self.seq_to_name[seq].add(name)
        self.name_to_seq[name] = seq
    
    def load_from_file(self, path):
        with open(path, "rt") as i:
            self.load_from_fasta(i)

    def load_from_url(self, url):
        logging.getLogger().info("\nDownloading list of known contaminants from {}".format(url))
        if url.startswith("file:"):
            return self.load_from_file(url[5:])
        else:
            return self.load_from_fasta(urlopen(url).read().decode().split("\n"))
    
    def load_from_fasta(self, fasta):
        """
        Returns a dict of seq:set(names)
        """
        close = False
        if isinstance(fasta, str):
            fasta = open(fasta, 'rt')
            close = True
        with FastaReader(fasta) as fasta:
            for record in fasta:
                name = record.name.split(None, 1)[0]
                seq = record.sequence
                self.add(name, seq)
        if close:
            fasta.close()
    
    @property
    def names(self):
        return list(self.name_to_seq.keys())
    
    @property
    def sequences(self):
        return list(self.seq_to_name.keys())
    
    def iter_names(self):
        return self.name_to_seq.items()
    
    def iter_sequences(self):
        return self.seq_to_name.items()
    
    def has_name(self, name):
        return name in self.name_to_seq
    
    def get_for_name(self, name):
        return self.name_to_seq[name]
    
    def has_seq(self, seq):
        return seq in self.seq_to_name
    
    def get_for_seq(self, seq):
        return list(self.seq_to_name[seq])
