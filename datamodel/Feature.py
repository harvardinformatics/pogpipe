import os
import sys
import shutil
import os.path
import logging

"""  

"""

class Feature(object):

    """Object that stores a group of Features with a common query"""

    def __init__(self):

        self.type1                 = "feature"
        self.type2                 = "feature"

        self.qid                   = None                  
        self.qstart                = -1
        self.qend                  = -1
        self.qdesc                 = None
        self.qlen                  = -1
        self.qcov                  = -1

        self.score                 = 0
        self.frame                 = 0
        self.strand                = 0
        self.phase                 = 0
        self.pid                   = 0

        self.hid                   = None
        self.hstart                = -1
        self.hend                  = -1
        self.hlen                  = -1
        self.hcov                  = -1

        self.qseq                  = None
        self.hseq                  = None
       
        self.hitattr               = {}


    def contains(self,gff):

        if self.qstart <= gff.qstart and self.qend >= gff.qend:
            return True
        else:
            return False
        
    def overlaps(self,gff):
        #print "%d %d %d %d"%(self.qstart,self.qend,gff.qstart,gff.qend)
        if not (self.qend < gff.qstart or
                self.qstart > gff.qend):
            return True
        else:
            return False

    def header_str(self):
        str = "QID\tType1\tType2\tQstart\tQend\tScore\tStrand\tPhase\tHID\tHstart\tHend\tQlen\tHlen\tQseq\tHseq\tPID"

 	return str

    def __str__(self):

	str = "%s\t%s\t%s\t%d\t%d\t%f\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%f"%(self.qid,self.type1,self.type2,self.qstart,self.qend,self.score,self.strand,self.phase,self.hid,self.hstart,self.hend,self.qlen,self.hlen,self.qseq,self.hseq,self.pid)

 	return str
