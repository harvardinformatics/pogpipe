 
"""Test for DB.py"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from datamodel.FileUtils        import FileUtils
from config                     import settings

from datamodel.database.AnalysisUtils import AnalysisUtils
from datamodel.database.DB            import init_database
from datamodel.database.DB            import Analysis, AnalysisInputFile, AnalysisOutputFile, AnalysisExpectedOutputFile 
from datamodel.database.DB            import AnalysisStatus,AnalysisCommand,AnalysisOutputString,AnalysisSummaryValue,AnalysisSlurmValue
from sqlalchemy.orm                   import sessionmaker



class DBCreateTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):
        
        if FileUtils.fileExists(settings.TESTDBNAME):  os.remove(settings.TESTDBNAME)

        settings.DBNAME = settings.TESTDBNAME

        init_database()
                    
        Session = sessionmaker(bind=settings.ENGINE)
        self.session = Session()


    def testCreateAnalysis(self):
        
        input_files = ['pog1.fa','pog2.fa','pog3.fa']
        input_types = ['fasta','fasta','fasta']
        
        obj1 = Analysis(name="pog1")
        obj2 = Analysis(name="pog2",currentstatus="COMPLETE")
        obj3 = Analysis(name="pog3")

        if1 = AnalysisInputFile(input_file='pog1.fa',input_file_rank=1)
        if2 = AnalysisInputFile(input_file='pog2.fa',input_file_rank=2)
        
        obj1.input_files.append(if1)
        obj1.input_files.append(if2)
        
        AnalysisUtils.setInputFiles(obj1,input_files,input_types)
        
        self.session.add(obj1)
        self.session.add(obj2)
        self.session.add(obj3)

        self.session.commit()

        self.assertTrue(obj1.id   == 1)
        self.assertTrue(obj2.name == "pog2")
        self.assertTrue(obj2.currentstatus == "COMPLETE")

        obj = self.session.query(Analysis).filter_by(name='pog1').all()

        self.assertTrue(len(obj) ==1)
        self.assertTrue(obj[0].id ==1)

        self.assertTrue(obj[0].currentstatus == "NEW")

        obj = self.session.query(Analysis).filter_by(currentstatus='NEW').all()

        self.assertTrue(len(obj) ==2)

        for key,value in obj[0].__dict__.items():
            print key,value

        print obj[0].status
        
    def tearDown(self):
        self.session.commit()
        self.session.close()

if __name__ == "__main__":                           # And run the file
    unittest.main()   
