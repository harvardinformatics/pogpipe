import sys

from   datamodel.Analysis       import Analysis

class DirectorySizeAnalysis(Analysis):
    """Toy class that find the size of a directory"""

    name = "DirectorySize"

    def __init__(self):
        super(DirectorySizeAnalysis,self).__init__(self.name)

    def getCommands(self):
        cmds = []

        for input in self.input:
            cmd = "du -sh " + input
            
            cmds.append(cmd)

        return cmds


