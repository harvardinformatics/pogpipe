"""Unit test for GTFTest.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.FileReader import FileReader

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):
        self.file = "../testdata/test.gtf"

    def testGTFFile(self):

        """Check we can read a file line by line """

        fr = FileReader(self.file)

        self.assertTrue(fr)

        line = fr.nextLine()

        while line:
            line = fr.nextLine()

        lines = fr.lnum

        self.assertTrue(lines == 1000)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
