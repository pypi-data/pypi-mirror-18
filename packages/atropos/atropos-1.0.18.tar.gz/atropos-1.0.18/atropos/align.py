# coding: utf-8
"""
Alignment module.
"""
from collections import namedtuple
from ._align import Aligner, compare_prefixes, locate, MultiAligner
from .util import reverse_complement, RandomMatchProbability

# flags for global alignment

# The interpretation of the first flag is:
# An initial portion of seq1 may be skipped at no cost.
# This is equivalent to saying that in the alignment,
# gaps in the beginning of seq2 are free.
#
# The other flags have an equivalent meaning.
START_WITHIN_SEQ1 = 1
START_WITHIN_SEQ2 = 2
STOP_WITHIN_SEQ1 = 4
STOP_WITHIN_SEQ2 = 8

# Use this to get regular semiglobal alignment
# (all gaps in the beginning or end are free)
SEMIGLOBAL = START_WITHIN_SEQ1 | START_WITHIN_SEQ2 | STOP_WITHIN_SEQ1 | STOP_WITHIN_SEQ2

def compare_suffixes(s1, s2, wildcard_ref=False, wildcard_query=False):
    """
    Find out whether one string is the suffix of the other one, allowing
    mismatches. Used to find an anchored 3' adapter when no indels are allowed.
    """
    s1 = s1[::-1]
    s2 = s2[::-1]
    _, length, _, _, matches, errors = compare_prefixes(s1, s2, wildcard_ref, wildcard_query)
    return (len(s1) - length, len(s1), len(s2) - length, len(s2), matches, errors)

# Common match-result object returned by aligners

class Match(object):
    """
    TODO creating instances of this class is relatively slow and responsible for quite some runtime.
    """
    __slots__ = ['astart', 'astop', 'rstart', 'rstop', 'matches', 'errors', 'front', 'adapter', 'read', 'length']
    def __init__(self, astart, astop, rstart, rstop, matches, errors, front=None, adapter=None, read=None):
        self.astart = astart
        self.astop = astop
        self.rstart = rstart
        self.rstop = rstop
        self.matches = matches
        self.errors = errors
        self.front = self._guess_is_front() if front is None else front
        self.adapter = adapter
        self.read = read
        # Number of aligned characters in the adapter. If there are indels,
        # this may be different from the number of characters in the read.
        self.length = self.astop - self.astart
        assert self.length > 0
        assert self.length - self.errors > 0
        if self.adapter:
            assert self.errors / self.length <= self.adapter.max_error_rate

    def __str__(self):
        return 'Match(astart={0}, astop={1}, rstart={2}, rstop={3}, matches={4}, errors={5})'.format(
            self.astart, self.astop, self.rstart, self.rstop, self.matches, self.errors)
    
    def copy(self):
        return Match(self.astart, self.astop, self.rstart, self.rstop, self.matches, self.errors,
                     self.front, self.adapter, self.read)
    
    def _guess_is_front(self):
        """
        Return whether this is guessed to be a front adapter.

        The match is assumed to be a front adapter when the first base of
        the read is involved in the alignment to the adapter.
        """
        return self.rstart == 0

    def wildcards(self, wildcard_char='N'):
        """
        Return a string that contains, for each wildcard character,
        the character that it matches. For example, if the adapter
        ATNGNA matches ATCGTA, then the string 'CT' is returned.

        If there are indels, this is not reliable as the full alignment
        is not available.
        """
        wildcards = [ self.read.sequence[self.rstart + i:self.rstart + i + 1] for i in range(self.length)
            if self.adapter.sequence[self.astart + i] == wildcard_char and self.rstart + i < len(self.read.sequence) ]
        return ''.join(wildcards)

    def rest(self):
        """
        Return the part of the read before this match if this is a
        'front' (5') adapter,
        return the part after the match if this is not a 'front' adapter (3').
        This can be an empty string.
        """
        if self.front:
            return self.read.sequence[:self.rstart]
        else:
            return self.read.sequence[self.rstop:]
    
    # TODO: write test
    def get_info_record(self):
        seq = self.read.sequence
        qualities = self.read.qualities
        if qualities is None:
            qualities = ''
        rsize = rsize_total = self.rstop - self.rstart
        if self.front and self.rstart > 0:
            rsize_total = self.rstop
        elif not self.front and self.rstop < len(seq):
            rsize_total = len(seq) - self.rstart
        return MatchInfo(
            self.read.name,
            self.errors,
            self.rstart,
            self.rstop,
            seq[0:self.rstart],
            seq[self.rstart:self.rstop],
            seq[self.rstop:],
            self.adapter.name,
            qualities[0:self.rstart],
            qualities[self.rstart:self.rstop],
            qualities[self.rstop:],
            self.front,
            self.astop - self.astart,
            rsize, rsize_total
        )

MatchInfo = namedtuple("MatchInfo", (
    "read_name", "errors", "rstart", "rstop", "seq_before", "seq_adapter", "seq_after",
    "adapter_name", "qual_before", "qual_adapter", "qual_after", "is_front", "asize",
    "rsize_adapter", "rsize_total"
))

# Alternative semi-global alignment (
# http://www.bioinf.uni-freiburg.de/Lehre/Courses/2013_SS/V_Bioinformatik_1/lecture4.pdf)
# strategies designed to improve insert matching of paired-end reads.
#
# Note: these are currently just prototype implementations. They will need to be optimized
# using numpy and/or re-written in cython.
#
# 1. SeqPurge algorithm: insert match algorithm that performs thresholded exhaustive
#    comparison to minimize probability of incorrect alignment. Relies on the fact that
#    overlapping reads share alleles and indels (i.e. no gaps are required) (in C++).
#    https://github.com/imgag/ngs-bits/tree/master/src/SeqPurge.
#   * Speed up sequence comparison:
#     * Between adapters and overhangs:
#       * http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4080745/pdf/btu177.pdf
#     * Between reads:
#       * http://bioinformatics.oxfordjournals.org/content/30/14/2000.abstract
# 2. Skewer algorithm: bit-masked k-difference matching (in C++).
#    https://github.com/relipmoc/skewer
# 3. Quality-aware overlap alignment (in Haskell).
#    https://hackage.haskell.org/package/bio-0.5.3/docs/Bio-Alignment-QAlign.html
# 4. FOGSAA, modified for semi-global alignment.
#    http://www.nature.com/articles/srep01746
#    http://www.isical.ac.in/~bioinfo_miu/FOGSAA.7z
#
# Also think about different sequence encodings that might enable faster alignment
# https://github.com/hammerlab/kerseq/blob/master/kerseq/sequence_encoding.py

class InsertAligner(object):
    """
    Implementation of an insert matching algorithm.
    This only works with paired-end reads with 3' adapters.
    """
    def __init__(self, adapter1, adapter2, match_probability=RandomMatchProbability(),
                 insert_max_rmp=1E-6, adapter_max_rmp=0.001,
                 min_insert_overlap=1, max_insert_mismatch_frac=0.2,
                 min_adapter_overlap=1, max_adapter_mismatch_frac=0.2,
                 adapter_check_cutoff=9, base_probs=dict(p1=0.25, p2=0.75)):
        self.adapter1 = adapter1
        self.adapter1_len = len(adapter1)
        self.adapter2 = adapter2
        self.adapter2_len = len(adapter2)
        self.match_probability = match_probability
        self.insert_max_rmp = insert_max_rmp
        self.adapter_max_rmp = adapter_max_rmp
        self.min_insert_overlap = min_insert_overlap
        self.max_insert_mismatch_frac = float(max_insert_mismatch_frac)
        self.min_adapter_overlap = min_adapter_overlap
        self.max_adapter_mismatch_frac = float(max_adapter_mismatch_frac)
        self.adapter_check_cutoff = adapter_check_cutoff
        self.base_probs = base_probs
        self.aligner = MultiAligner(
            max_insert_mismatch_frac,
            START_WITHIN_SEQ1 | STOP_WITHIN_SEQ2,
            min_insert_overlap)
    
    def match_insert(self, seq1, seq2):
        """Use cutadapt aligner for insert and adapter matching"""
        l1 = len(seq1)
        l2 = len(seq2)
        seq_len = min(l1, l2)
        if l1 > l2:
            seq1 = seq1[:l2]
        elif l2 > l1:
            seq2 = seq1[:l1]

        seq2_rc = reverse_complement(seq2)
        
        def _match(insert_match, offset, insert_match_size, prob):
            if offset < self.min_adapter_overlap:
                # The reads are mostly overlapping, to the point where
                # there's not enough overhang to do a confident adapter
                # match. We return just the insert match to signal that
                # error correction can be done even though no adapter
                # trimming is required.
                return (insert_match, None, None)
            
            # TODO: this is very sensitive to the exact correct choice of adapter.
            # For example, if you specifiy GATCGGAA... and the correct adapter is
            # AGATCGGAA..., the prefixes will not match exactly and the alignment
            # will fail. We need to use a comparison that is a bit more forgiving.
            
            a1_match = compare_prefixes(seq1[insert_match_size:], self.adapter1)
            a2_match = compare_prefixes(seq2[insert_match_size:], self.adapter2)
            adapter_len = min(offset, self.adapter1_len, self.adapter2_len)
            max_adapter_mismatches = round(adapter_len * self.max_adapter_mismatch_frac)
            if a1_match[5] > max_adapter_mismatches and a2_match[5] > max_adapter_mismatches:
                return None
            
            a1_prob = self.match_probability(a1_match[4], adapter_len)
            a2_prob = self.match_probability(a2_match[4], adapter_len)
            if (adapter_len > self.adapter_check_cutoff) and ((a1_prob * a2_prob) > self.adapter_max_rmp):
                return None

            adapter_len1 = min(self.adapter1_len, l1 - insert_match_size)
            adapter_len2 = min(self.adapter2_len, l2 - insert_match_size)
            best_adapter_matches, best_adapter_mismatches = (a1_match if a1_prob < a2_prob else a2_match)[4:6]
            
            return (
                insert_match,
                Match(0, adapter_len1, insert_match_size, l1, best_adapter_matches, best_adapter_mismatches),
                Match(0, adapter_len2, insert_match_size, l2, best_adapter_matches, best_adapter_mismatches)
            )
        
        # # This is the old way of doing things, where we use the built-in
        # # Aligner to do a single match.
        # aligner = Aligner(
        #     seq2_rc,
        #     self.max_insert_mismatch_frac,
        #     START_WITHIN_SEQ1 | STOP_WITHIN_SEQ2,
        #     False, False)
        # aligner.min_overlap = self.min_insert_overlap
        # aligner.indel_cost = 100000
        #
        # insert_match = aligner.locate(seq1)
        #
        # if not insert_match:
        #     return None
        #
        # offset = min(insert_match[0], seq_len - insert_match[3])
        # insert_match_size = seq_len - offset
        # prob = self.match_probability(insert_match[4], insert_match_size)
        #
        # if prob > self.insert_max_rmp:
        #     return None
        #
        # return _match(insert_match, offset, insert_match_size, prob)
        
        # Use an aligner that returns all matches that satisfy the
        # overlap and error rate thresholds. We sort by matches and
        # then mismatches, and then check each in turn until we find
        # one with an adapter match (if any).
        
        insert_matches = self.aligner.locate(seq2_rc, seq1)
        
        if insert_matches:
            # Filter by random-match probability
            filtered_matches = []
            for insert_match in insert_matches:
                offset = min(insert_match[0], seq_len - insert_match[3])
                insert_match_size = seq_len - offset
                prob = self.match_probability(insert_match[4], insert_match_size, **self.base_probs)
                if prob <= self.insert_max_rmp:
                    filtered_matches.append((insert_match, offset, insert_match_size, prob))
            
            if filtered_matches:
                if len(filtered_matches) == 1:
                    return _match(*filtered_matches[0])
                else:
                    # Test matches in order of random-match probability.
                    # TODO: compare against sorting by length (which is how
                    # SeqPurge essentially does it).
                    #filtered_matches.sort(key=lambda x: x[2], reverse=True)
                    filtered_matches.sort(key=lambda x: x[3])
                    for m in filtered_matches:
                        match = _match(*m)
                        if match:
                            return match
            
            return None
