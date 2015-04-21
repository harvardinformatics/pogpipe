from argparse  import ArgumentParser

import importlib
import logging
import os
import sys
import csv
import pprint

from datamodel.factory.GFFFactory import GFFFactory
from datamodel.factory.FastaFile  import FastaFile

from config import settings

def main(args):

    logging.info(" ========> parsing GFFFile")

    logging.info("ARGS %s"%args)

    gfffilename   = args.gfffile
    fastafilename = args.fastafile

    gff_factory = GFFFactory(gfffilename)
    fastafile   = FastaFile(fastafilename)


    seqs = {}

    seq = fastafile.nextSeq()

    while seq is not None:
        seqs[seq['id']] = seq['seq']
        seq = fastafile.nextSeq()


    gff = gff_factory.nextGFF()

    while gff is not  None:
        hid = gff.hitattr['ID']
        #print "%s\t%s\t%s\t%d\t%d\t%f\t%d\t%s\t%s"%(gff.qid,gff.type1,gff.type2,gff.qstart,gff.qend,gff.score,gff.strand,gff.phase,hid)
        if gff.type2 == "CDS":
            seq = seqs[gff.qid]
            seq = seq[gff.qstart-1:gff.qend]

            #print "%d\t%s"%(gff.strand,seq)

            newseq = translate(seq,gff.strand)
            print ">%s\n%s"%(hid,newseq)


        gff = gff_factory.nextGFF()


def translate(seq,strand):
    map = {"TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L",
           "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S",
           "TAT":"Y", "TAC":"Y", "TAA":"*", "TAG":"*",
           "TGT":"C", "TGC":"C", "TGA":"*", "TGG":"W",
           "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
           "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
           "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
           "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R",
           "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M",
           "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T",
           "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K",
           "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R",
           "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V",
           "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A",
           "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E",
           "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G",}

    newseq = ""

    if strand == -1:
        seq = revcomp(seq)


    i = 0
    while i < len(seq)-2:
        if seq[i:i+3] in map:
            newseq = newseq + map[seq[i:i+3]]
        else:
            newseq = newseq + "X"

        i += 3

    return newseq
        
def revcomp(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    reverse_complement = "".join(complement.get(base, base) for base in reversed(seq))

    return reverse_complement

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Parse GFF file into features and translate')

    parser.add_argument('-g', '--gfffile'   , help='GFF file to parse')
    parser.add_argument('-f', '--fastafile'   , help='Fasta file to use as sequence source')
    
    args = parser.parse_args()

    main(args)

