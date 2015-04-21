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
        self.qstart                = None
        self.qend                  = None
        self.qdesc                 = None
        self.qseq                  = None
        self.qlen                  = None
        self.qcov                  = None

        self.score                 = 0
        self.frame                 = 0
        self.strand                = 0
        self.phase                 = 0
        self.pid                   = 0

        self.hid                   = None
        self.hstart                = None
        self.hend                  = None
        self.hseq                  = None
        self.hlen                  = None
        self.hcov                  = None

        self.qseq                  = None
        self.hseq                  = None
       
        self.hitattr               = {}
    def __str__(self):
	
	str = "%s\t%s\t%s\t%d\t%d\t%f\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%f\n"%(self.qid,self.type1,self.type2,self.qstart,self.qend,self.score,self.strand,self.phase,self.hid,self.hstart,self.hend,self.qlen,self.hlen,self.qseq,self.hseq,self.pid) 

 	return str
