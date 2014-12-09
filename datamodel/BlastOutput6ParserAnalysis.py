from   datamodel.Analysis       import Analysis
from   datamodel.FileUtils      import FileUtils
from   datamodel.Feature        import Feature
from   datamodel.FeatureSet     import FeatureSet
from   subprocess               import Popen, PIPE
from   config                   import settings

import os
import re
import logging

class BlastOutput6ParserAnalysis(Analysis):

    """Class that takes blast output format 6 (tabular) and parses it into queries and hits"""

    minimum_space_needed = 1000000

    name       = "BlastOutput6Parser"

    def __init__(self):

        super(BlastOutput6ParserAnalysis,self).__init__(self.name)


    def setInputFiles(self,input_files,input_types):
        super(BlastOutput6ParserAnalysis,self).setInputFiles(input_files,input_types)

    def init(self):

        if len(self.input_files) == 0:
            raise Exception("No input files for BlastOutput6Parsermodule. Can't init")

        fileparts = FileUtils.getFileParts(self.input_files[0])

        
    def getCommands(self):

        self.checkDiskSpace()

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        return self.commands
    
    def postProcessOutput(self):

        super(BlastOutput6ParserAnalysis,self).postProcessOutput()

        data   = {}

        file   = self.input_files[0]

        with open(file) as fp:

            for line in fp:

                line = line.rstrip('\n')
                ff   = line.split('\t')

                qid = ff[0]
                hid = ff[1]
                pid = float(ff[2])
                alnlen = ff[3]
                mm     = int(ff[4])
                gaps   = int(ff[5])
                qstart = int(ff[6])
                qend   = int(ff[7])
                hstart = int(ff[8])
                hend   = int(ff[9])
                exval   = float(ff[10])
                score  = float(ff[11])

                feat = Feature()

                feat.qid = qid
                feat.qstart = qstart
                feat.qend   = qend
                feat.hid    = hid
                feat.hstart = hstart
                feat.hend   = hend

                feat.pid = pid
                feat.score = score
                
                feat.mm = mm
                feat.gaps = gaps
                feat.exval = exval

                if len(ff) > 12:
                    feat.qlen = int(ff[12])
                    feat.hlen = int(ff[13])
                    feat.qseq = ff[14]
                    feat.hseq = ff[15]

                if not qid in data:
                    data[qid] = []

                tmp = data[qid]

                tmp.append(feat)

            self.data = data


        print "#QID\t$HID\tQCOV\tHCOV\tPID\tSCORE\tQSEQ\tHSEQ"
        for qid in self.data:
            i = 0
            for hfeat in self.data[qid]:
                hcov = 100*(hfeat.hend-hfeat.hstart+1)/hfeat.hlen
                qcov = 100*(hfeat.qend-hfeat.qstart+1)/hfeat.qlen

                if i < 1:
                    print "%s\t%s\t%d\t%d\t%f\t%f\t%s\t%s"%(qid,hfeat.hid,qcov,hcov,hfeat.pid,hfeat.score,hfeat.qseq, hfeat.hseq)
                
                i = i + 1
            print "\n";
        return data
                    


                    
                    
