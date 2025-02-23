"""Unit test for FastQCAnalysis.py"""

import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from   datamodel.AnalysisRunner          import AnalysisRunner
from   datamodel.FastQCAnalysis          import FastQCAnalysis
from   datamodel.factory.AnalysisFactory import AnalysisFactory

from   config                            import settings

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    
    def setUp(self):

        self.input_files = ["../testdata/FoxP2_SL167.fastq"]
        self.input_types = ['fastq']

    def testRun(self):

        self.ana = AnalysisFactory.createAnalysisFromModuleName("FastQC")

        self.ana.setInputFiles(self.input_files,self.input_types)

        self.assertTrue(len(self.input_files) == 1)
        self.assertTrue(len(self.input_types) == 1)

        cmds = self.ana.getCommands()

        print cmds

        self.assertTrue(len(cmds) == 1)

        runner = AnalysisRunner(self.ana)

        res = runner.run()

        self.assertTrue(res)

        self.ana.postProcessOutput()

        output_str = self.ana.output_str
        
        self.assertTrue(len(output_str) == 4)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
