"""Unit test for Analysis.py"""

import os
import sys
import unittest
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from config                    import    settings
from datamodel.FileUtils       import    FileUtils
from datamodel.database.DB     import    Analysis, init_database
from datamodel.database.AnalysisUtils import AnalysisUtils
from sqlalchemy.orm            import sessionmaker

if FileUtils.fileExists(settings.TESTLOGFILE):   os.remove(settings.TESTLOGFILE)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh        = logging.FileHandler(settings.TESTLOGFILE, 'a')
fh.setFormatter(formatter)

log = logging.getLogger()  # root logger
        
for hdlr in log.handlers:  # remove all old handlers
    log.removeHandler(hdlr)
            
log.addHandler(fh)      # set the new handler

class DBAnalysisTest(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):
        
        if FileUtils.fileExists(settings.TESTDBNAME):    os.remove(settings.TESTDBNAME)
        
        settings.DBNAME  = settings.TESTDBNAME
                
        init_database()
        
        #input_files = ['pog1.fa','pog2.fa','pog3.fa']
        #input_types = ['fasta','fasta','fasta']
        #self.ana = Analysis("FastQC")

        self.input_files = ["testdata/FoxP2_SL167.fastq"]
        self.input_types = ['fastq']
        
        Session      = sessionmaker(bind=settings.ENGINE)
        self.session = Session()


    def testCreateAnalysis(self):

        obj1 = Analysis(name="pog1")
        obj2 = Analysis(name="pog2",currentstatus="COMPLETE")
        obj3 = Analysis(name="pog3")

        AnalysisUtils.setInputFiles(obj1,self.input_files,self.input_types)
        obj1.output_dir = "/tmp"
        obj1.working_dir = "/tmp"
        obj1.init()
        
    def testSaveAndQueryAnalysis(self):
        
        obj1 = Analysis(name="pog1")
        obj2 = Analysis(name="pog2",currentstatus="COMPLETE")
        obj3 = Analysis(name="pog3")

        AnalysisUtils.setInputFiles(obj1,self.input_files,self.input_types)
        
        self.session.add(obj1)
        self.session.add(obj2)
        self.session.add(obj3)

        self.session.commit()
        
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
