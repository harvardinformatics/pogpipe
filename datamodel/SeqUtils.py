import os
import sys
import shutil
import os.path
import datetime
import tempfile

class SeqUtils(object):

    """Bag of methods for sequence analysis/manipulation.  Translation, reverse complementing etc -  """

    
    """ Blatantly stolen from BioPython """

    standardCodonTable = {'name':     'Standard',
                          'alt_name': 'SGC0', 
                          'id':       1,
                          'table': {
            'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S',
            'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y',
            'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
            'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
            'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I',
            'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 'ACC': 'T',
            'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K',
            'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
            'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
            'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D',
            'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
            'GGG': 'G', },
                          'stop_codons':  ['TAA', 'TAG', 'TGA', ],
                          'start_codons': ['TTG', 'CTG', 'ATG', ]
                          }
    
    comps = {}
    comps['A'] = 'T'
    comps['T'] = 'A'
    comps['G'] = 'C'
    comps['C'] = 'G'
    comps['a'] = 't'
    comps['t'] = 'a'
    comps['g'] = 'c'
    comps['c'] = 'g'
    

    @staticmethod
    def translate(str):

        i = 0
        
        pep = ""
        
        while i < len(str)-2:
            
            codon = str[i:i+3]
            
            if codon in SeqUtils.standardCodonTable['table']:
                res = SeqUtils.standardCodonTable['table'][codon]
            else:
                res = "X"
                
                
            pep = pep + res
                
            i = i + 3
                
        return pep

    @staticmethod
    def reverseComplement(seqstr):

        i = 0
        newstr = ""
        while i < len(seqstr):
            ch = seqstr[i]

            if ch in SeqUtils.comps:
                newstr = newstr +  SeqUtils.comps[ch]
            else:
                newstr = newstr + ch

            i = i + 1

        return newstr[::-1]

