import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

class TupleTest(unittest.TestCase):

    def setUp(self):

        self.months = ("January","February","March","April","May","June","July","August","September","October","November","December")

    def testTuple(self):
	self.assertTrue(len(self.months) == 12)

if __name__ == "__main__":                           # And run the file
    unittest.main()   
