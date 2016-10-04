"""Unit test for LastzFile.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.LastzFile import LastzFile
from datamodel.Feature   import Feature
from datamodel.FileUtils import FileUtils

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):
        self.lastzfile = "../testdata/test1.lastz"
        self.lastzfile = "../testdata/test2.lastz"

    def testBlatFile(self):

        """Check we can read a lastz general output file """

        lastzobj = LastzFile(self.lastzfile)

        self.assertTrue(lastzobj)

        feat = lastzobj.nextFeature()

        while feat:
            feat = lastzobj.nextFeature()
            
        qfeat  = lastzobj.queryfeat
        qnum   =  len(qfeat.keys())

        tfeat  = lastzobj.targetfeat
        tnum   = len(tfeat.keys())


        for qid in qfeat:

#            print "QID %s"%qid

            tmpfeat = qfeat[qid]

            tophit = None
            topcov = 0
            tophcov = 0
            toppid  = 0

            for tmpf in tmpfeat:
 #               print tmpf

                qlen    = tmpf.qlen
                hlen    = tmpf.hlen

                qcov = tmpf.hitattr['cov']
                pid = tmpf.hitattr['pid']

                if qcov > topcov:

                    topcov = qcov
                    tophit = tmpf
                    toppid = pid

            print("%s\t%s\t%d\t%d"%(qid,tophit.hid,topcov,toppid))

        print qnum
        print tnum
        #self.assertTrue(qnum == 74)
        #self.assertTrue(tnum == 49)


                          
if __name__ == "__main__":                           # And run the file
    unittest.main()   
