import os
import sys
import os.path
import logging
import importlib
from   subprocess      import Popen, PIPE
from   config          import settings

class FastaFile(object):
   
    fh  = None
    id  = None
    seq = None

    def __init__(self,file):
       self.fh = open(file)


    def nextSeq(self):
      for line in self.fh:

        if line is None:
           return

        line = line.rstrip('\n')
        ff   = line.split(' ')

        if ff[0].startswith(">"):
          id = ff[0].replace(">",'')
              
          seq = {}
          found = 0
          if self.seq is not None:

            seq['id']  = self.id
            seq['seq'] = self.seq
            found = 1

          self.id  = id
          self.seq = None

          if found == 1:
            return seq
        else:
          if self.seq is None:
            self.seq = line
          else:
            self.seq = self.seq + line

      if self.id is not None:
        seq = {}

        seq['id']  = self.id
        seq['seq'] = self.seq

        self.id = None
        self.seq = None
        return seq

 

    def calcProfile(self,seqs):

       seqlen = len(seqs[0]['seq'])

       print "LEn %d"%seqlen
       counts = []

       i = 0

       while i < seqlen:

         tmpcounts = {}

         j = 0;

         while j < len(seqs):

            char = seqs[j]['seq'][i]
            if char not in tmpcounts:
               tmpcounts[char] = 0

            tmpcounts[char] = tmpcounts[char]+1

            j = j + 1

       print "I %d %d %s"%(i,j,tmpcounts)
       counts.append(tmpcounts)

       i = i + 1


       return counts


















