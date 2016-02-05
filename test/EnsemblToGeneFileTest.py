"""Unit test for EnsemblToGeneFile.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.EnsemblToGeneFile import EnsemblToGeneFile
from datamodel.FileUtils import FileUtils

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):
        self.enstogenefile = "../testdata/mm10.ensemblToGenename.txt"

    def testEnsemblToGeneFile(self):

        """Check we can read an EnsemblToGene file """

        e2g = EnsemblToGeneFile(self.enstogenefile)

        self.assertTrue(e2g)

        self.assertTrue(len(e2g.geneids) == 38803)
        self.assertTrue(len(e2g.tranids) == 94647)



if __name__ == "__main__":                           # And run the file
    unittest.main()   
