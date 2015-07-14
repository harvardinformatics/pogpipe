import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.FileUtils     import FileUtils

class FileUtilsTest(unittest.TestCase):

    def setUp(self):

        self.mydir      = "/tmp/"
        self.mybasename = "myfile"
        self.mysuffix   = ".txt"
        self.text       = "Here is some text"

    def testGetDatestampedFilename(self):

        """ Takes a directory, basename and suffix and inserts a datestamp before the suffix """

        filename = FileUtils.getDatestampedFilename(self.mydir,self.mybasename,self.mysuffix)

        print filename

        self.assertTrue(filename)

    def testWriteTextToFile(self):

        """ Writes text to a filename """

        filename = FileUtils.getDatestampedFilename(self.mydir,self.mybasename,self.mysuffix)


        FileUtils.writeTextToFile(filename,self.text)

    def testFileExists(self):

        """ Tests existence of a file """

        filename = FileUtils.getDatestampedFilename(self.mydir,self.mybasename,self.mysuffix)

        FileUtils.writeTextToFile(filename,self.text)

        self.assertTrue(filename)

    def testGetFileParts(self):

        filename = self.mydir + self.mybasename + self.mysuffix

        fparts = FileUtils.getFileParts(filename)

        print fparts

        self.assertTrue(fparts['fileext'] == self.mysuffix)

    #def testGetDiskUsage(dir):

    #def testGetPercentFreeDiskSpace(dir):

    #def testGetFreeDiskSpace(dir):

    #def testGetFreeGbDiskSpace(dir):

    #def testGetOnlyFilesInDirectory(path):

    #def getAllFilesInDirectory(path):

if __name__ == "__main__":                           # And run the file
    unittest.main()   
