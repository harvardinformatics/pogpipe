import os
import re
import sys
import os.path
import logging
import importlib
from   subprocess      import Popen, PIPE
from   config          import settings

class FastaFilter(object):
   
    @classmethod
    def filterById(self,seqs,pattern):

        tmpseqs = []

        j = 0

        while j < len(seqs):
            id = seqs[j]['id']

            if re.match(pattern,id) is not None:
                tmpseqs.append(seqs[j])
                
            j = j+ 1

        return tmpseqs


            
    



