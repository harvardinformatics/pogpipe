"""Unit test for AnalysisRunner.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.AnalysisRunner          import AnalysisRunner
from datamodel.database.DB             import Analysis
from datamodel.factory.AnalysisFactory import AnalysisFactory


class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):

        self.factory = AnalysisFactory()
        self.ana     = self.factory.createAnalysisFromModuleName("Bowtie2")
        self.ana.param   = " -x ../testdata/databases/Arabidopsis_TAIR.9.171 "

        self.ana.setInputFiles(["../testdata/FoxP2_SL167.fastq"],['fastq'])

    def testCreateNewAnalysisRunner(self):           # Function gets called automatically

        """New instance should create successfully"""

        anarun = AnalysisRunner(self.ana)

        tmpinputs = anarun.analysis.getInputFiles()

        self.assertTrue(anarun)

    def testRun(self):

        anarun = AnalysisRunner(self.ana)

        res = anarun.run()

        self.assertTrue(res)

    def testGetOutput(self):
        anarun = AnalysisRunner(self.ana)

        res = anarun.run()

        anarun.analysis.postProcessOutput()

        out = anarun.analysis.output_files

        print out
        print anarun.analysis.summary_data

        self.assertTrue(len(out) == 2)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
