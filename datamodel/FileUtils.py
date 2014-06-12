import os
import sys
import shutil
import os.path
import datetime
import tempfile

class FileUtils(object):

    """Bag of methods for directory listings,  splitting filenames apart etc """

    
    @staticmethod
    def fileExists(file):
        if os.path.isfile(file):
            return True
        else:
            return False
        
    @staticmethod    
    def getFileParts(file):
        
        basename  = os.path.basename(file)
        dirname   = os.path.dirname(file)
        
        (filestub,fileext) = os.path.splitext(basename)
        
        return {'basename':  basename,
                'dirname':   dirname,
                'filestub':  filestub,
                'fileext':   fileext,
                }

    @staticmethod
    def getDiskUsage(dir):
        
        st = os.statvfs(dir)

        free  = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used  = (st.f_blocks - st.f_bfree) * st.f_frsize

        out = {'free'  :free,
               'total' :total,
               'used'  : used,
               }

        return out

    @staticmethod
    def getPercentFreeDiskSpace(dir):

        out = FileUtils.getDiskUsage(dir)

        return out['free']*100/out['total']

    @staticmethod
    def getFreeDiskSpace(dir):

        out = FileUtils.getDiskUsage(dir)

        return out['free']

    @staticmethod
    def getFreeGbDiskSpace(dir):

        out = FileUtils.getDiskUsage(dir)

        return out['free']/1000000000

    @staticmethod
    def getOnlyFilesInDirectory(path):

        return [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]


    @staticmethod
    def getAllFilesInDirectory(path):

        return os.listdir(path)

    @staticmethod
    def getDatestampedFilename(dir,basename,suffix):

        if suffix[0] != '.':
            suffix = "." + suffix
        
        suffix   = "." + datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S") + suffix

        filename = os.path.join(dir, basename + suffix)
        
        return filename

    @staticmethod
    def writeTextToFile(filename,text):

        with open(filename, "w") as text_file:
            text_file.write(text)


    @staticmethod
    def checkDirExists(dir):

        if not os.path.isdir(dir):
            os.makedirs(dir)

    @staticmethod
    def checkDirExistsForFile(filename):

        dir = os.path.dirname(filename)

        FileUtils.checkDirExists(dir)
