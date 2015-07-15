import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.Slurm     import Slurm

from   config                              import settings
from   datamodel.Analysis                  import Analysis
from   datamodel.factory.AnalysisFactory   import AnalysisFactory

class SlurmTest(unittest.TestCase):

    def setUp(self):
        self.input = []
        self.input.append("testdata/FoxP2_SL167.fastq");

        self.analysis  = AnalysisFactory.createAnalysisFromModuleName("FastQC")

        self.analysis.setInputFiles(self.input,['fastq'])

    def testCreateSbatchFile(self):

        analysis = self.analysis

        slurm = Slurm(analysis)

        slurm.createSbatchFile()

        print slurm.batchfile
        print slurm.batchfiletext

if __name__ == "__main__":                           # And run the file
    unittest.main()   



