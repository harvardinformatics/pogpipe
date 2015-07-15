"""Unit test for AnalysisDB.py"""

import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.AnalysisDBFactory import AnalysisDBFactory
from datamodel.factory.AnalysisFactory   import AnalysisFactory
from datamodel.Analysis                  import Analysis

import pprint

from config import settings

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):
        self.dbobj    = AnalysisDBFactory(settings.TESTDBNAME)
        self.ana_fact = AnalysisFactory()
        self.anaobj   = self.ana_fact.createAnalysisFromModuleName("FastQC")

        self.anaobj.setInputFiles(["../testdata/FoxP2_SL167.fastq"],['fastq'])

    def testCreateObject(self):
        """ Test we can create a new AnalysisDBFactory object """

        self.assertTrue(self.dbobj)


    def testCreateAnalysisTables(self):
        """ Test we can create the Analysis tables """

        self.assertTrue(self.dbobj.createAnalysisTables())


    def testGetTables(self):

        """ Test we can retrive a list of db tables """

        self.dbobj.createAnalysisTables()
        rows = self.dbobj.getTables()
        self.assertTrue(len(rows) == 9)

    def testAddAnalysisToDB(self):

        """ Test we can save an Analysis object to the DB """

        #self.dbobj.createAnalysisTables()
        #self.dbobj.saveAnalysis(self.anaobj)

        #self.assertTrue(1)

    def testFetchAnalsyisFromDB(self):

        """ Test we can fetch an existing analysis object from the DB"""

        #self.anaobj.id = None
        #self.dbobj.saveAnalysis(self.anaobj)
        
        #ana = self.dbobj.fetchAnalysisByID(self.anaobj.id)

        #str1 = self.anaobj.toString()
        #str2 = ana.toString()

        #self.assertTrue(str1 == str2)

    def testUpdateAnalysisStatus(self):

        """ Test updating an analysis objects status"""

        self.anaobj.id = None
        self.dbobj.saveAnalysis(self.anaobj)

        
        self.dbobj.updateAnalysisStatus(self.anaobj,"RUNNING")


        ana = self.dbobj.fetchAnalysisByID(self.anaobj.id)

        str1 = self.anaobj.toString()
        str2 = ana.toString()

        print "STR1 %s" % str1
        print "STR2 %s" % str2

        self.assertTrue(ana.current_status == "RUNNING")

if __name__ == "__main__":                           # And run the file
    unittest.main()   
