import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.SeqUtils     import SeqUtils

class SeqUtilsTest(unittest.TestCase):

    def setUp(self):
        self.seq1 = "ATCGCNNXX"
        self.seq2 = "ATGCCGACTCGTRTCCGATGTAA"


    def testReverseComplement(self):

        revcomp = SeqUtils.reverseComplement(self.seq1)

        self.assertTrue(revcomp == 'XXNNGCGAT')

    def testTranslate(self):
        trans   = SeqUtils.translate(self.seq2)

        self.assertTrue(trans == 'MPTRXRC')


if __name__ == "__main__":                           # And run the file
    unittest.main()   
