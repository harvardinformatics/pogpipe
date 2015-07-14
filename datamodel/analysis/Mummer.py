from   datamodel.Analysis       import Analysis
from   datamodel.FileUtils      import FileUtils
from   subprocess               import Popen, PIPE
from   config                   import settings

import os
import re
import logging

class Mummer(Analysis):

    """Class that has all the info to run mummer on two fasta files"""

    minimum_space_needed = 1000000

    name          = "Mummer"
    bindir        = settings.TOOLDIR  + "MUMmer3.23"
    nucmerfile    = bindir  +"/nucmer" 

    params        = {'maxgap': 500,
                     'mincluster': 100,
                     }

    def __init__(self):

        super(Mummer,self).__init__(self.name)

        self.params['prefix'] = self.output_dir + "/mummer"

    def getCommands(self):
        
        if len(self.input_files) != 2:
            raise Exception("Mummer module needs 2 input files. Can't init")

        self.checkDiskSpace()

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        command = self.nucmerfile

        for key,value in self.params.items():
            command = command + " --"+str(key) + "=" + str(value)


        command = command + " " + self.input_files[0] + " " + self.input_files[1]

        self.commands.append(command)

        return self.commands
    
