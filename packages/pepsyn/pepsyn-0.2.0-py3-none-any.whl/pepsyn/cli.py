# Copyright 2016 Uri Laserson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from logging import captureWarnings

# biopython has a bunch of annoying warnings bc Seq comparisons changed
captureWarnings(True)

from click import group, command, option, argument, File, Choice
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from pepsyn.operations import (
    reverse_translate, remove_site_from_cds, x_to_ggsg, disambiguate_iupac_aa,
    tile as tile_op)
from pepsyn.codons import (
    FreqWeightedCodonSampler, UniformCodonSampler, ecoli_codon_usage)
from pepsyn.util import site2dna


@group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """pepsyn -- peptide synthesis design"""
    pass


# reusable args
argument_input = argument('input', type=File('r'))
argument_output = argument('output', type=File('w'))


@cli.command()
@argument_input
@argument_output
@option('--length', '-l', type=int, help='Length of output oligos')
@option('--overlap', '-p', type=int, help='Overlap of oligos')
def tile(input, output, length, overlap):
    """tile a set of sequences"""
    for seqrecord in SeqIO.parse(input, 'fasta'):
        for (start, end, t) in tile_op(seqrecord.seq, length, overlap):
                output_title = '{}|{}-{}'.format(seqrecord.id, start, end)
                output_record = SeqRecord(t, output_title, description='')
                SeqIO.write(output_record, output, 'fasta')


@cli.command()
@argument_input
@argument_output
@option('--prefix', '-p', help='DNA sequence to prefix each oligo')
def prefix(input, output, prefix):
    """add a prefix to each sequence"""
    for seqrecord in SeqIO.parse(input, 'fasta'):
        newseq = prefix + seqrecord.seq
        seqrecord.seq = newseq
        SeqIO.write(seqrecord, output, 'fasta')


@cli.command()
@argument_input
@argument_output
@option('--suffix', '-s', help='DNA sequence to suffix each oligo')
def suffix(input, output, suffix):
    """add a suffix to each sequence"""
    for seqrecord in SeqIO.parse(input, 'fasta'):
        newseq = seqrecord.seq + suffix
        seqrecord.seq = newseq
        SeqIO.write(seqrecord, output, 'fasta')


@cli.command()
@argument_input
@argument_output
@option('--codon-table', '-t', default='standard',
        help='ONLY STANDARD TABLE IMPLEMENTED')
@option('--codon-usage', '-u', default='ecoli', help='ONLY ECOLI IMPLEMENTED')
@option('--sampler', default='weighted', show_default=True,
        type=Choice(['weighted', 'uniform']), help='Codon sampling method')
def revtrans(input, output, codon_table, codon_usage, sampler):
    """reverse translate amino acid sequences into DNA"""
    if sampler == 'weighted':
        codon_sampler = FreqWeightedCodonSampler(usage=ecoli_codon_usage)
    elif sampler == 'uniform':
        codon_sampler = UniformCodonSampler()
    for seqrecord in SeqIO.parse(input, 'fasta'):
        dna_id = seqrecord.id
        dna_seq = reverse_translate(seqrecord.seq, codon_sampler)
        SeqIO.write(SeqRecord(dna_seq, dna_id, description=''), output, 'fasta')


@cli.command()
@argument_input
@argument_output
@option('--site', help='Site to remove (e.g., EcoRI, AGCCT); case sensitive')
@option('--clip-left', type=int,
        help='Number of bases to clip from start of sequence to get to CDS')
@option('--clip-right', type=int,
        help='Number of bases to clip from end of sequence to get to CDS')
@option('--codon-table', '-t', default='standard',
        help='ONLY STANDARD TABLE IMPLEMENTED')
@option('--codon-usage', '-u', default='ecoli', help='ONLY ECOLI IMPLEMENTED')
@option('--sampler', default='weighted', show_default=True,
        type=Choice(['weighted', 'uniform']), help='Codon sampling method')
def removesite(input, output, site, clip_left, clip_right, codon_table,
               codon_usage, sampler):
    """remove site from each sequence's CDS by recoding"""
    if sampler == 'weighted':
        codon_sampler = FreqWeightedCodonSampler(usage=ecoli_codon_usage)
    elif sampler == 'uniform':
        codon_sampler = UniformCodonSampler()

    # import pdb; pdb.set_trace()
    site = site2dna(site)
    # site is now a Bio.Seq.Seq

    for seqrecord in SeqIO.parse(input, 'fasta'):
        id_ = seqrecord.id
        cds_start = clip_left
        cds_end = len(seqrecord) - clip_right
        seq = remove_site_from_cds(seqrecord.seq, site, codon_sampler,
                                   cds_start, cds_end)
        SeqIO.write(SeqRecord(seq, id_, description=''), output, 'fasta')


@cli.command()
@argument_input
@argument_output
def x2ggsg(input, output):
    """replace stretches of Xs with Serine-Glycine linker (GGSG pattern)"""
    for seqrecord in SeqIO.parse(input, 'fasta'):
        seq = seqrecord.seq
        replacement = x_to_ggsg(seq)
        seqrecord.seq = replacement
        if replacement != seq:
            seqrecord.id = '{}|{}'.format(seqrecord.id, 'withGSlinker')
        SeqIO.write(seqrecord, output, 'fasta')


@cli.command()
@argument_input
@argument_output
def disambiguateaa(input, output):
    """replace ambiguous (IUPAC) AAs with unambiguous ones (e.g. Z => E/Q)

    B => DN, X => ACDEFGHIKLMNPQRSTVWY, Z => EQ, J => LI,
    U => C (selenocysteine), O => K (pyrrolysine)
    """
    for seqrecord in SeqIO.parse(input, 'fasta'):
        id_ = seqrecord.id
        ambig = seqrecord.seq
        for (i, unambig) in enumerate(disambiguate_iupac_aa(ambig)):
            if unambig != ambig:
                seqrecord.id = '{}|disambig_{}'.format(id_, i + 1)
                seqrecord.seq = unambig
            SeqIO.write(seqrecord, output, 'fasta')


@cli.command()
@argument_input
@option('--site', help='Site to find (e.g., EcoRI, AGCCT); case sensitive')
def findsite(input, site):
    """find locations of a site"""
    query = site2dna(site)
    for seqrecord in SeqIO.parse(input, 'fasta'):
        id_ = seqrecord.id
        idx = seqrecord.seq.find(query)
        if idx >= 0:
            print('{}|{}|{}'.format(id_, site, idx), flush=True)


@cli.command()
@argument_input
def stats(input):
    """NOT IMPL'd: compute some sequence statistics"""
    pass
