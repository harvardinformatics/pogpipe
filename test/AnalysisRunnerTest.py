"""Unit test for AnalysisRunner.py"""

from datamodel.AnalysisRunner          import AnalysisRunner
from datamodel.Analysis                import Analysis
from datamodel.factory.AnalysisFactory import AnalysisFactory
import unittest


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
