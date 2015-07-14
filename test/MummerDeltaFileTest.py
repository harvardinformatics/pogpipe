"""Test for Mummer.py"""

import unittest
import os
import sys

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.analysis.MummerDeltaFile import MummerDeltaFile
from datamodel.factory.FastaFile        import FastaFile
from datamodel.FileUtils                import FileUtils


class MummerTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):

        self.deltafile = '../testdata/mummer/mummer1.delta'

        self.input_files = ['../testdata/mummer/GCA_000163955.1_ASM16395v1_genomic.fna',
                            '../testdata/mummer/GCA_000341505.1_ASM34150v1_genomic.fna']


    def testCreateMummerDeltaFile(self):

        refseqs = FastaFile.getSequenceDict(self.input_files[0])
        qryseqs = FastaFile.getSequenceDict(self.input_files[1])

        self.assertTrue(len(refseqs) == 87)
        self.assertTrue(len(qryseqs) == 34)

        mdf = MummerDeltaFile(self.deltafile,refseqs,qryseqs)

        self.assertTrue(mdf)


        mdf.parse()
        
        
        

        
if __name__ == "__main__":                           # And run the file
    unittest.main()   
