"""Unit test for GTFTest.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.BlatFile import BlatFile
from datamodel.Feature   import Feature
from datamodel.FileUtils import FileUtils

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):
        self.blatfile = "../testdata/testsmall.blat.psl"
        self.blatfile = "../testdata/mm10.over350.fastMap.psl"

    def testBlatFile(self):

        """Check we can read a blat psl file """

        blatobj = BlatFile(self.blatfile)

        self.assertTrue(blatobj)

        feat = blatobj.nextFeature()

        while feat:
            feat = blatobj.nextFeature()
            
        qfeat  = blatobj.queryfeat
        qnum   =  len(qfeat.keys())

        tfeat  = blatobj.targetfeat
        tnum   = len(tfeat.keys())


        for qid in qfeat:

#            print "QID %s"%qid

            tmpfeat = qfeat[qid]

            tophit = None
            topcov = 0
            tophcov = 0

            for tmpf in tmpfeat:
 #               print tmpf
                match = tmpf.hitattr['match']
                mismatch = tmpf.hitattr['mismatch']

                qlen    = tmpf.qlen
                hlen    = tmpf.hlen

                qcov = int(100*(match+mismatch)/qlen)
                hcov = int(100*(match+mismatch)/hlen)
                pid = int(100*match/(match+mismatch))

                if qcov > topcov:

                    topcov = qcov
                    tophit = tmpf

                elif qcov == topcov:
                    if hcov > tophcov:
                        #print "Found greater hcov"
                        tophcov = hcov
                        tophit = tmpf

            print tophit

        self.assertTrue(qnum == 227)
        self.assertTrue(tnum == 554)


                          
if __name__ == "__main__":                           # And run the file
    unittest.main()   
