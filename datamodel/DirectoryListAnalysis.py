import sys

from   datamodel.database.DB   import Analysis, AnalysisCommand

class DirectoryListAnalysis(Analysis):
    """Toy class that lists the contents of a directory"""

    name = "DirectoryList"

    def __init__(self):
        super(DirectoryListAnalysis,self).__init__()

    def getCommands(self):
        
        return map(lambda x: AnalysisCommand(command="ls " + x.input_file), self.input_files)




