"""Unit test for Bowtie2Analysis.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from   datamodel.database.AnalysisUtils   import AnalysisUtils
from   datamodel.AnalysisRunner           import AnalysisRunner
from   datamodel.Bowtie2Analysis          import Bowtie2Analysis
from   datamodel.factory.AnalysisFactory  import AnalysisFactory

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 
    
    def setUp(self):

        self.input_files = ["../testdata/FoxP2_SL167.fastq"]
        self.input_types = ['fastq']
        self.param       = " -x ../testdata/databases/Arabidopsis_TAIR.9.171 "

    def testRun(self):

        self.ana = AnalysisFactory.createAnalysisFromModuleName("Bowtie2")
        
        AnalysisUtils.setInputFiles(self.ana,self.input_files,self.input_types)
        self.ana.init()  #  This does the defaults but should be in the constructor
        
        self.ana.param = self.param

        self.assertTrue(len(self.input_files) == 1)
        self.assertTrue(len(self.input_types) == 1)

        cmds = self.ana.getCommands()

        self.assertTrue(len(cmds) == 2)

        runner = AnalysisRunner(self.ana)

        res = runner.run()

        self.assertTrue(res)

        self.ana.postProcessOutput()

        output_str = self.ana.output_strings

        print len(output_str)

        self.assertTrue(len(output_str) == 1)

        print self.ana.summary_data

        self.assertTrue(self.ana.summary_data['Number_of_Reads'] == '3')
        self.assertTrue(self.ana.summary_data['Aligned 0 Times'] == '3')


if __name__ == "__main__":                           # And run the file
    unittest.main()   
