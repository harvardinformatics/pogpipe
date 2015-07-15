 
"""Test for DB.py"""

import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptdir + "/../")

from datamodel.FileUtils        import FileUtils
from config                     import settings

if FileUtils.fileExists(settings.TESTDBNAME):
    os.remove(settings.TESTDBNAME)

settings.DBNAME = settings.TESTDBNAME


from datamodel.database.DB      import Analysis, AnalysisInputFile
from sqlalchemy.orm             import sessionmaker

class DBCreateTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):
        
            
        Session = sessionmaker(bind=settings.ENGINE)
        self.session = Session()


    def testCreateAnalysis(self):
        
        obj1 = Analysis(name="pog1")
        obj2 = Analysis(name="pog2",currentstatus="COMPLETE")
        obj3 = Analysis(name="pog3")

        if1 = AnalysisInputFile(input_file='pog1.fa',input_file_rank=1)
        if2 = AnalysisInputFile(input_file='pog2.fa',input_file_rank=2)
        
        obj1.input_files.append(if1)
        obj1.input_files.append(if2)
        
        
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
