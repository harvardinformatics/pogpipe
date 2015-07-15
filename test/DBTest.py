 
"""Test for DB.py"""

import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")


from datamodel.database.DB      import Analysis,Base
from datamodel.FileUtils        import FileUtils

from sqlalchemy                 import create_engine
from sqlalchemy.orm             import sessionmaker

from config import settings

if FileUtils.fileExists(settings.TESTDBNAME):
    os.remove(settings.TESTDBNAME)

class DBCreateTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):

        self.engine      = create_engine('sqlite:///test.db')
        self.engine.echo = True

        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)

        self.session = Session()


    def testCreateAnalysis(self):
        
        obj1 = Analysis(name="pog1")
        obj2 = Analysis(name="pog2",currentstatus="COMPLETE")
        obj3 = Analysis(name="pog3")


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
