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

        self.features = []
        self.qid                   = None                  
        self.qstart                = None
        self.qend                  = None
        self.qdesc                 = None
        self.qseq                  = None
        self.qlen                  = None
        self.qcov                  = None

        self.score                 = None
        self.frame                 = None
        self.strand                = None
        self.pid                   = None

        self.hid                   = None
        self.hstart                = None
        self.hend                  = None
        self.hseq                  = None
        self.hlen                  = None
        self.hcov                  = None

        self.qseq                  = None
        self.hseq                  = None
        
