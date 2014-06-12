import sys

from   datamodel.Analysis       import Analysis

class DirectoryListAnalysis(Analysis):
    """Toy class that lists the contencts of a directory"""

    name = "DirectoryList"

    def __init__(self):
        super(DirectoryListAnalysis,self).__init__(self.name)

    def getCommands(self):
        cmds = []

        for input in self.input_files:
            cmd = "ls " + input
            
            cmds.append(cmd)

        self.commands = cmds

        return cmds


