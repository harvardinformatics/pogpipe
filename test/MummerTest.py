"""Test for Mummer.py"""

import unittest
import os
import sys

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.analysis.Mummer import Mummer
from datamodel.AnalysisRunner  import AnalysisRunner
from datamodel.Feature         import Feature
from datamodel.FileUtils       import FileUtils
from datamodel.database.AnalysisUtils import AnalysisUtils

class MummerTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):

        self.input_files = ['../testdata/mummer/GCA_000163955.1_ASM16395v1_genomic.fna',
                            '../testdata/mummer/GCA_000341505.1_ASM34150v1_genomic.fna']


    def testCreateMummer(self):

        mummer = Mummer()

        self.assertTrue(mummer)
        self.assertTrue(AnalysisUtils.setInputFiles(mummer,self.input_files,['fasta','fasta']))

        mummer.init()
        tmpfiles = AnalysisUtils.getInputFiles(mummer)

        self.assertTrue(len(tmpfiles) ==2)

        commands = mummer.getCommands()

        print commands

        self.assertTrue(len(commands) == 1)

        self.assertTrue(commands[0].command.index('tools/macosx/MUMmer3.23/nucmer --maxgap=500 --mincluster=100') > 0)

    def testRunMummer(self):

        
        mummer = Mummer()

        self.assertTrue(mummer)
        self.assertTrue(AnalysisUtils.setInputFiles(mummer,self.input_files,['fasta','fasta']))

        runner = AnalysisRunner(mummer)
        

        self.assertTrue(runner.run())

        self.assertTrue(len(mummer.output_strings) == 1)

        self.assertTrue(mummer.output_strings[0].output_string.index('4: FINISHING DATA') > 0)


        self.assertTrue(FileUtils.fileExists('../testout/mummer.delta'))


        
    def tearDown(self):

        deltafile = '../testout/mummer.delta'

        if FileUtils.fileExists(deltafile):
            os.remove(deltafile)
            

        
if __name__ == "__main__":                           # And run the file
    unittest.main()   
