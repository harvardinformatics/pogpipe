import os
import sys
import os.path
import logging
import importlib
from   subprocess      import Popen, PIPE
from   config          import settings

class FastaFile(object):
   
    fh   = None
    id   = None
    seq  = None
    seqs = []

    def __init__(self,file):
       self.filename = file
       self.fh = open(file)

    
    def calcStats(self):
       self.calcSeqlen()
       self.calcProfile()
       self.calcConsensus()

       self.calcCoverageAndPID()

       outstr = ""

       j = 0

       outstr = outstr +  "\n%s\t%40s\t%s\t%s\n"%(self.filename,"ID","Cov","PID")

       while j < len(self.seqs):

          tmpcov = self.coverage[j]
          tmppid = self.percentid[j]
          tmpid  = self.seqs[j]['id']

          outstr = outstr +  "%s\t%40s\t%d\t%d"%(self.filename,tmpid,tmpcov,tmppid)

          j = j + 1

       outstr = outstr + "\n"
       outstr = outstr + self.prettyPrint()
       outstr = outstr + "\n"

       # Only really relevant when we have more than 2 sequences.

       if len(self.seqs) > 2:
           outstr = outstr +  "Calculating mutation distribution for [%s] sequences"%(len(self.seqs))
           self.calcMutationDist()
       elif len(self.seqs) == 2:
           outstr = outstr +  "Calculating pairwise mutation distribution for [%s] sequences"%(len(self.seqs))
           self.calcPairwiseMutationProfile()

    def calcPairwiseMutationProfile(self):

        # We want the following
        #   - consensus length, seq1 id, seq2 id, seq1 length, seq2 length, no of matches, no of differences, no indels in seq1 no indels in seq2, seq1 coverage, seq2 coverage, percent identity
        
        if self.consensus is None:
            raise Exception("No consensus sequence - can't calculate pairwise mutation profile for %s"%self.filename)

        if len(self.seqs) != 2:
            raise Exception("Number of sequences mismatch [%s].  Need 2 sequences to calculate pairwise mutation profile for "%self.filename)


        outstr  = ""

        conslen = len(self.consensus)

        seq1    = self.seqs[0]
        seq2    = self.seqs[1]

        len1    = len(seq1['seq'])
        len2    = len(seq2['seq'])

        match1    = 0
        match2    = 0

        mismatch1 = 0
        mismatch2 = 0

        indel1    = 0
        indel2    = 0

        pid       = 0
        
        charcount1 = 0
        charcount2 = 0
        i = 0
               
        while i < self.seqlen:
            cons_c = self.consensus[i]

            char1  = seq1['seq'][i]
            char2  = seq2['seq'][i]

            #print "CHARS %c %c %c"%(char1,char2,cons_c)

            if char1 != '-':
                charcount1 = charcount1 + 1

            if char2 != '-':
                charcount2 = charcount2 + 1

            if char1 != '-' and char2 != '-':


                if char1 == cons_c:
                    #print "MAtch 1 %c %c"%(char1,cons_c)
                    match1 = match1 + 1
                    
                else:
                    mismatch1 = mismatch1 + 1


                if char2 == cons_c:
                    #print "MAtch 2 %c %c"%(char1,cons_c)
                    match2 = match2 + 1
                else:
                    mismatch2 = mismatch2 + 1
                    

            elif char1 == '-':
                indel1 = indel1 + 1

            elif char2 == '-':
                indel2 = indel2 + 1

            else:
                # We shouldn't get here
                raise Exception("Something's wrong comparing characters.  We shouldn'get get here [%c] [%c] in file [%s]"%(char1,char2,self.filename))

            i = i + 1

        pid1 = int(100*match1/(match1+mismatch1))
        pid2 = int(100*match2/(match2+mismatch2))

        cov1 = int(100*charcount1/conslen)
        cov2 = int(100*charcount2/conslen)
                
#        print "PAIRMUT %40s %40s %40s %4d %4d %4d %4d %5d %5d %5d %5d %5d %5d"%("Filename","ID1","ID2","Pos","C1","C2","Found","NG1","NG2","Cons_M","Coverage","Percentid")
        outstr = outstr +  "PAIRMUT %40s %40s %40s %4s %4s %10s %6s %8s %6s %6s %5s %5s %5s %5s\n"%("Filename","ID1","ID2","Len1","Len2","conslen","Match","Mismatch","Indel1","Indel2","Cov1","Cov2","PID1","PID2")
        print "PAIRMUT %40s %40s %40s %4d %4d %10d %6d %8d %6d %6d %5d %5d %5d %5d"%(self.filename,seq1['id'],seq2['id'],len(seq1['seq']),len(seq2['seq']),conslen,match1,mismatch1,indel1,indel2,cov1,cov2,pid1,pid2)

        j = 0


    def calcMutationDist(self):

        #print len(self.seqs) 
        #print self.seqlen

        print "MUT %40s %40s %40s %4s %4s %4s %4s %5s %5s %5s %12s %20s %20s"%("Filename","ID1","ID2","Pos","C1","C2","C3","Found","NG1","NG2","Cons_M","Coverage","Percentid")
        j = 0
        while j < len(self.seqs):

           k = 0;

           while k < j:

              # We are comparing the chars in seq j and seq k

              # We want to know :

              #     - How many positions are there in the sequence where the char is the same in j and k but not in the others
              #     - Where are these positions

              i = 0
               
              while i < self.seqlen:
                  c_j = self.seqs[j]['seq'][i]
                  c_k = self.seqs[k]['seq'][i]

                  jj     = 0
                  found  = 0 
                  foundc = '-'

                  while  jj < len(self.seqs):

                     c_jj = self.seqs[jj]['seq'][i]
                 
                     if jj != j and jj != k:

                         if c_jj != c_j and c_jj != c_k:

                            if c_j == c_k:
                                 found = 1
                                 foundc = c_jj
                     jj = jj + 1

                  if found == 1:

                    ischar1 = 1
                    ischar2 = 1

                    if c_j != '-' and c_k != '-':
                       ischar1 = 0

                    if foundc != '-':
                       ischar2 = 0

                    print "MUT %40s %40s %40s %4d %4c %4c %4c %5d %5d %5d %12d %12s %12s"%(self.filename,self.seqs[j]['id'],self.seqs[k]['id'],i,c_j,c_k,foundc,found,ischar1,ischar2,self.cons_meth,'\t'.join(str(x) for x in self.coverage),'\t'.join(str(x) for x in self.percentid))

                  i = i + 1

              k = k+ 1

	   j = j + 1


    def calcSeqlen(self):     
       seqlen = -1

       for seq in self.seqs:
           if len(seq['seq']) > seqlen:
             seqlen = len(seq['seq'])
     
       self.seqlen = seqlen

    def calcProfile(self):
       # Profile


       i = 0

       profile = []
       total  = []

       cons_meth = 1
       
       while i < self.seqlen:
         profile.append({})
         total.append({})

         total[i]['total']  = 0
         total[i]['indels'] = 0
         total[i]['chars']  = 0

         j = 0

         while j < len(self.seqs):
             
             c = self.seqs[j]['seq'][i]
           
             if c not in profile[i]:
                profile[i][c] = 0

             profile[i][c] = profile[i][c] + 1 
             total[i]['total'] = total[i]['total'] + 1

             if c == '-':
               total[i]['indels'] = total[i]['indels'] + 1
             else:
               total[i]['chars'] = total[i]['chars'] + 1
               
             if i == 0 and c != 'M':
                cons_meth = 0 
                            
             j = j+ 1

         i = i + 1

       self.profile = profile
       self.total   = total
       self.cons_meth = cons_meth

    def calcConsensus(self):
       # Consensus sequence 

       consensus = []

       i = 0

       while i < self.seqlen:

          maxcount = -1
          maxchar  = '-'
 
          for c in self.profile[i]:

             if c != '-':

               if self.profile[i][c] > maxcount:
                  maxchar = c
                  maxcount = self.profile[i][c]

          consensus.append(c)

          i = i + 1

       self.consensus = consensus                 
              
    def calcCoverageAndPID(self):
       coverage  = []
       percentid = []

       j = 0
       while j < len(self.seqs):

          i   = 0
          cov = 0
          match = 0
          mismatch = 0

          while i < self.seqlen:
             conschar = self.consensus[i]

             c = self.seqs[j]['seq'][i]
             if c != '-':
                cov = cov + 1

                if c == conschar:
                   match = match+1
                else:
                   mismatch = mismatch+1  

             i = i + 1

          cov = int(100*cov/self.seqlen)
          pid = int(100*match/(match+mismatch))

          coverage.append(cov)
          percentid.append(pid)

          j = j + 1

       self.coverage   = coverage
       self.percentid  = percentid

    def prettyPrint(self):

       outstr = ""
       str = []

       j = 0;

       consstr = ''.join(self.consensus)

 
       while j < len(self.seqs):

          tmpstr = []
          i = 0

          while i < self.seqlen:

              c = self.seqs[j]['seq'][i]

              if c == self.consensus[i]:
                 tmpstr.append('.')
              else:
                 tmpstr.append(c)
              
              i = i+1
          str.append(tmpstr)
          
          j = j + 1

       str.append(consstr)

       i = 0

       while i < self.seqlen:
           j = 0 
           outstr = outstr +  "%40s %s\n"%("Consensus",consstr[i:i+80])
           while j < len(self.seqs):
               outstr = outstr + "%40s %s\n"%(self.seqs[j]['id'],''.join(str[j][i:i+80]))
               j = j + 1
               outstr = outstr +  "\n" 
           i = i + 80

       return outstr

    @staticmethod
    def toString(seqs):

       str    = []
       seqlen = -1

       j = 0

       for seq in seqs:

           if len(seq['seq']) > seqlen:
               seqlen = len(seq['seq'])
           j = j + 1

       for seq in seqs:
           str.append(">%s"%seq['id'])
           i = 0
           while i < len(seq['seq']):
               str.append(''.join(seq['seq'][i:i+80]))
               i = i + 80
           j = j + 1

       string = '\n'.join(str)

       return string
           
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
            self.seqs.append(seq)
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
        self.seqs.append(seq)
        return seq

 

    def calcProfile2(self,seqs):

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

 
















