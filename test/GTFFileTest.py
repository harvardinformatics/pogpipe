"""Unit test for GTFTest.py"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.GTFFile import GTFFile
from datamodel.Feature   import Feature
from datamodel.FileUtils import FileUtils

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 

    def setUp(self):
        self.gtffile = "../testdata/test.gtf"
        self.gtffile = "../testdata/mm10.ucsc.ensGene.gtf"

    def testGTFFile(self):

        """Check we can read a gtf file """

        gtfobj = GTFFile(self.gtffile)

        self.assertTrue(gtfobj)

        genes = {}

        geneid = gtfobj.nextGene()

        while geneid:
            print "##### GENE %s #####"%geneid
            trans = gtfobj.genes[geneid]

            print "Number of transcripts %d"%(len(trans.keys()))

            maxtranid = gtfobj.getLongestTranscript(geneid)

            print "MAX TRAN %s %s"%(maxtranid,geneid)

            for tranid in trans:
                maxstr = "---"
                if tranid == maxtranid:
                    maxstr = "MAX"

                print "transcript %s %s %d"%(maxstr,tranid,len(trans[tranid]))

                tlen = 0
                for ex in trans[tranid]:
                    if ex.type2 == "exon":
                        tlen += ex.qend-ex.qstart+1
                        print "Exon %d"%(ex.qend-ex.qstart+1)
                        
                print "Transcript %s %s Exons %d Length %d"%(maxstr,tranid,len(trans[tranid]),tlen)



            geneid = gtfobj.nextGene()
            
        print "Number of genes [%d]"%len(gtfobj.genes.keys())

        self.assertTrue(len(gtfobj.genes.keys())== 27)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
