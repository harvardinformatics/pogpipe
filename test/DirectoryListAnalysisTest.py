"""Unit test for DirectoryListAnalysis.py"""

import unittest
import os
import sys

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from   datamodel.DirectoryListAnalysis import DirectoryListAnalysis
from   datamodel.AnalysisRunner        import AnalysisRunner

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    
    def setUp(self):

        self.inputs = ['/tmp']
        
        self.anaobj = DirectoryListAnalysis()


    def testSetInputFiles(self):

        self.assertTrue(self.anaobj.setInputFiles(self.inputs,['dir']))

    def testGetInput(self):

        self.anaobj.setInputFiles(self.inputs,['dir'])

        tmpinputs = self.anaobj.input_files

        self.assertEqual(len(tmpinputs),len(self.inputs)) # Assertion that the test framework collates

    def testRun(self):

        self.anaobj.setInputFiles(self.inputs,['dir'])

        self.runner  = AnalysisRunner(self.anaobj)    

        self.runner.run()

        
        tmpstr = self.anaobj.getOutputStrings()
        
        print tmpstr
        self.assertTrue(len(self.anaobj.getOutputStrings()) > 0)


    def testGetOutput(self):
        self.anaobj.setInputFiles(self.inputs,['dir'])

        self.runner  = AnalysisRunner(self.anaobj)    

        self.runner.run()

        out = self.runner.analysis.getOutputStrings()

        self.assertTrue(len(out)>0)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
