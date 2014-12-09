"""Unit test for Feature.py"""

from datamodel.Feature  import Feature
from datamodel.FileUtils import FileUtils
import unittest

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):

        self.feat = Feature()

        self.feat.qid = "chr1"
        self.feat.qstart = 10200
        self.feat.qend   = 10340
        self.feat.score  = 100
        self.feat.pid    = 90.0
        self.feat.qlen   = 100000000
        self.feat.qseq   = "NNN"
        self.feat.phase  = "."
        self.feat.strand = 1
        self.feat.hid    = "D89D80"
        self.feat.hstart = 1
        self.feat.hend   = 141
        self.feat.hlen   = 150
        self.feat.hseq   = "NNN"
      

    def testGetString(self):

        """Check the string representation for a feature """

        c = "%s"%(self.feat)
        print c
        self.assertTrue(1)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
