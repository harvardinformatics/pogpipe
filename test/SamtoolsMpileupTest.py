"""Unit test for SamtoolsMpileupAnalysis.py"""

import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from   datamodel.AnalysisRunner          import AnalysisRunner
from   datamodel.SamtoolsMpileupAnalysis import SamtoolsMpileupAnalysis
from   datamodel.factory.AnalysisFactory import AnalysisFactory

from   config                            import settings

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    
    def setUp(self):

        self.input_files = ["../testdata/ce10.chrX.15k-25k.bam"]
        self.input_types = ['bam']

        self.refgenome = "../testdata/databases/ce10.fa"

    def testRun(self):

        self.ana = AnalysisFactory.createAnalysisFromModuleName("SamtoolsMpileup")

        self.ana.setInputFiles(self.input_files,self.input_types)
        self.ana.refgenome = self.refgenome

        self.assertTrue(len(self.input_files) == 1)
        self.assertTrue(len(self.input_types) == 1)

        self.ana.init()

        cmds = self.ana.getCommands()

        print cmds

        self.assertTrue(len(cmds) == 2)

        runner = AnalysisRunner(self.ana)

        res = runner.run()

        self.assertTrue(res)

        self.ana.postProcessOutput()

        output_strings = self.ana.output_strings
        
        print "Output %d"%(len(output_strings))

        for strobj in output_strings:
            print "Output string %s"%strobj.output_string

        self.assertTrue(len(output_strings) == 1)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
