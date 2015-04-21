import os
import sys
import re
import os.path
import logging
import importlib

from   subprocess         import Popen, PIPE
from   config             import settings
from   datamodel.Feature  import Feature

class GFFFactory(object):
   
    fh   = None

    def __init__(self,file):
       self.filename = file
       self.fh = open(file)

    
    def nextGFF(self):

      for line in self.fh:

        if line is None:
           return

        if re.search('^#',line):
            continue

        line = line.rstrip('\n')
        ff   = line.split('\t')

##gff-version 3
#!gff-spec-version 1.20
#!processor NCBI annotwriter
#!genome-build ASM72083v1
#!genome-build-accession NCBI_Assembly:GCF_000720835.1
##sequence-region NZ_JODT01000001.1 1 388890
##species http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=67256
#NZ_JODT01000001.1       RefSeq  region  1       388890  .       +       .       ID=id0;Dbxref=taxon:67256;collection-date=2010;country=Japan: Suginami%2C Tokyo;culture-collection=NRRL:B-2120;gbkey=Src;isolation-source=garden soil;mol_type=genomic DNA;strain=NRRL B-2120;sub-species=achromogenes
#NZ_JODT01000001.1       RefSeq  gene    283     1188    .       -       .       ID=gene0;Name=IH25_RS0100010;gbkey=Gene;locus_tag=IH25_RS0100010
#NZ_JODT01000001.1       Protein Homology        CDS     283     1188    .       -       0       ID=cds0;Parent=gene0;Dbxref=Genbank:WP_030600633.1;Name=WP_030600633.1;gbkey=CDS;product=DeoR faimly transcriptional regulator;protein_id=WP_030600633.1;transl_table=11
#NZ_JODT01000001.1       RefSeq  gene    1391    2839    .       -       .       ID=gene1;Name=IH25_RS0100015;gbkey=Gene;locus_tag=IH25_RS0100015
#NZ_JODT01000001.1       Protein Homology        CDS     1391    2839    .       -       0       ID=cds1;Parent=gene1;Dbxref=Genbank:WP_030600636.1;Name=WP_030600636.1;Note=catalyzes the reduction of nonspecific electron acceptors such as 2%2C6-dimethyl-1%2C4-benzoquinone and 5-hydroxy-1%2C4-naphthaquinone%3B does not have lipoamide dehydrogenase activity;gbkey=CDS;product=flavoprotein disulfide reductase;protein_id=WP_030600636.1;transl_table=11
#NZ_JODT01000001.1       RefSeq  gene    2936    3373    .       +       .       ID=gene2;Name=IH25_RS0100020;gbkey=Gene;locus_tag=IH25_RS0100020
#NZ_JODT01000001.1       Protein Homology        CDS     2936    3373    .       +       0       ID=cds2;Parent=gene2;Dbxref=Genbank:WP_030600640.1;Name=WP_030600640.1;gbkey=CDS;product=gamma-glutamyl cyclotransferase;protein_id=WP_030600640.1;transl_table=11
#NZ_JODT01000001.1       RefSeq  gene    3499    4323    .       +       .       ID=gene3;Name=IH25_RS0100025;gbkey=Gene;locus_tag=IH25_RS0100025
#NZ_JODT01000001.1       Protein Homology        CDS     3499    4323    .       +       0       ID=cds3;Parent=gene3;Dbxref=Genbank:WP_03060

        if len(ff) < 8:
            raise Exception("GFF line needs 8 or more fields to parse")

        f = Feature()

        f.qid     = ff[0]
        f.type1   = ff[1]
        f.type2   = ff[2]
        f.qstart  = int(ff[3])
        f.qend    = int(ff[4])
        f.score   = ff[5]
        f.strand  = ff[6]
        f.phase   = ff[7]

        if f.score == ".":
            f.score = 0
        else:
            f.score = int(f.score)

        if f.strand == "+":
            f.strand = 1

        if f.strand == "-":
            f.strand = -1

        if f.strand == ".":
            f.strand = 0

        if len(ff) > 8:

            hidstr  = ff[8]
            hitattr = {}


            hffarr = hidstr.split(';')
            
            for hff in hffarr:

                tmparr = hff.split('=')

                hitattr[tmparr[0]] = tmparr[1]

            f.hitattr = hitattr

        return f


 
















