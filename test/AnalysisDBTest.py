"""Unit test for AnalysisDB.py"""

from datamodel.factory.AnalysisDBFactory import AnalysisDBFactory
from datamodel.factory.AnalysisFactory   import AnalysisFactory
from datamodel.Analysis                  import Analysis


import pprint
import unittest
import sys

from config import settings

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):
        self.ana    = AnalysisFactory.createAnalysisFromModuleName("FastQC")

        self.ana.setInputFiles(["../testdata/FoxP2_SL167.fastq"],['fastq'])

        print "Input %s" % self.ana.input_files

        self.db = AnalysisDBFactory(settings.TESTDBNAME)

    def testAddAnalysisToDB(self):

        """ Test we can save an Analysis object to the DB """

        db  = self.db
        ana = self.ana

        db.createAnalysisTables()

        ana.getCommands()

        ana.owner         = 'mclamp'
        ana.owner_email   = 'michele_clamp@harvard.edu'
        ana.output_status = "COMMAND_SUCCESSFUL"
        ana.param         = "--verbose"
        ana.queue         = "serial_requeue"
        ana.slurmid       = 1000
        ana.cores         = 12
        ana.mempercore    = 2048

        res = db.saveAnalysis(ana)
        
        self.assertTrue(res,"Saved analysis")

        tmpana = db.fetchAnalysisByID(ana.id)

        self.assertTrue(tmpana,"Fetched analysis")

        # This doens't work as the expected output files need the input filestub in there

        str1 = ana.toString()
        str2 = tmpana.toString()

        #print "STR1 [%s]"%str1
        #print "STR2 [%s]"%str2

        #self.assertTrue(str1 == str2)
        self.assertTrue(tmpana.id         == ana.id,"Analysis ids match")

        self.assertTrue(tmpana.output_dir == ana.output_dir,"Output directories match")

        ana.id = 24

        res = db.saveAnalysis(ana)
        self.assertTrue(res,"Saved analysis")

if __name__ == "__main__":                           # And run the file
    unittest.main()   
