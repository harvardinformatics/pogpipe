"""Unit test for Analysis.py"""

from datamodel.Analysis  import Analysis
from datamodel.FileUtils import FileUtils
import unittest

class ObjectCreateCheck(unittest.TestCase):          # Class with unitttest.TestCase as arg - 


    def setUp(self):

        self.ana = Analysis("FastQC")

        self.ana.setInputFiles(["testdata/FoxP2_SL167.fastq"],['fastq'])


    def testGetDiskUsage(self):

        """Check we can find the free disk space for our working directory"""

        out = FileUtils.getDiskUsage("/tmp/")

        print " Disk usage is %s " % out

        self.assertTrue(out > 0)

    def testGetPercentFreeDiskSpace(self):

        """Check we can find the free disk space for our working directory"""

        out = FileUtils.getPercentFreeDiskSpace("/tmp/")

        print " Percent free is %d" % out

        self.assertTrue(out >=0 and out <= 100)

    def testGetFreeDiskSpace(self):

        """Check we can find the free disk space for our working directory"""

        out = FileUtils.getFreeDiskSpace("/tmp/")

        print " Bytes free are %d" % out

        self.assertTrue(out > 0)

    def testGetFreeGbDiskSpace(self):

        """Check we can find the free disk space for our working directory"""

        out = FileUtils.getFreeGbDiskSpace("/tmp/")

        print " GBytes free are %d" % out

        self.assertTrue(out > 0)

    def testGetFilesInDirectory(self):

        """Check we can return an array of files in a directory"""

        files = FileUtils.getAllFilesInDirectory("/tmp/")

        self.assertTrue(len(files) > 0)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
