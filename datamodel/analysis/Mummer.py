from   datamodel.database.DB              import Analysis,AnalysisCommand
from   datamodel.database.AnalysisUtils   import AnalysisUtils
from   datamodel.analysis.MummerDeltaFile import MummerDeltaFile
from   datamodel.factory.FastaFile        import FastaFile
from   datamodel.FileUtils                import FileUtils
from   config                             import settings

import os
import re
import logging

class Mummer(Analysis):

    """Class that has all the info to run mummer on two fasta files"""

    minimum_space_needed = 1000000

    name          = "Mummer"
    bindir        = settings.TOOLDIR  + "MUMmer3.23"
    nucmerfile    = bindir  +"/nucmer" 

    paramhash        = {'maxgap': 500,
                     'mincluster': 100,
                     }

    def __init__(self):

        super(Mummer,self).__init__()

        self.paramhash['prefix'] = self.output_dir + "/mummer"

    def getCommands(self):
        
        if len(self.input_files) != 2:
            raise Exception("Mummer module needs 2 input files. Can't init")

        AnalysisUtils.checkDiskSpace(self)

        if AnalysisUtils.checkInputFiles(self) == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        command = self.nucmerfile

        for key,value in self.paramhash.items():
            command = command + " --"+str(key) + "=" + str(value)


        command = command + " " + self.input_files[0].input_file + " " + self.input_files[1].input_file

        self.commands.append(AnalysisCommand(command=command,command_rank=len(self.commands)+1))

        return self.commands
    

    @staticmethod
    def parseDeltaFile(deltafile,reffile,qryfile):

        if not FileUtils.fileExists(deltafile):
            raise Exception("Can't parse Mummer delta file.  File [%s] doesn't exist"%deltafile)

        if not FileUtils.fileExists(reffile):
            raise Exception("Can't parse Mummer delta file.  Reference fasta file [%s] doesn't exist"%reffile)

        if not FileUtils.fileExists(qryfile):
            raise Exception("Can't parse Mummer delta file.  Query fasta file [%s] doesn't exist"%qryfile)


        refseqs = FastaFile.getSequenceDict(reffile)
        qryseqs = FastaFile.getSequenceDict(qryfile)

        tmpmdf     = MummerDeltaFile(deltafile,refseqs,qryseqs)

        tmpmdf.parse()

        return tmpmdf.alns
