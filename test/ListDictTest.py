import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

class ListDictTest(unittest.TestCase):

    def setUp(self):

        self.mylist = []
        self.mydict = {}

        self.mylist.append("Pog")
        self.mylist.append(2)
        self.mylist.append(None)

        self.mydict['Pog'] = "Sog"
        self.mydict['Sog'] = None
        self.mydict['Log'] = 2

    def testList(self):

        """ Test we can loop over a list and quote the strings """

        newlist = []

        for i,val in enumerate(self.mylist):
            
            if isinstance(val,int):

                newlist.append(val)

            elif val is None:

                newlist.append("NULL")

            else:
                val =  "'" + val + "'"

                newlist.append(val)

        tmpstr =  "insert into AnalysisStatus(Name,Rank,Status) values(%s,%s,%s)"%(newlist[0],newlist[1],newlist[2])
        
        self.assertTrue(tmpstr == "insert into AnalysisStatus(Name,Rank,Status) values('Pog',2,NULL)")

    def test(self):

        """ Test we can loop over a dict and quote the strings """

        newdict = {}

        for key,val in self.mydict.iteritems():
            if isinstance(val,int):

                newdict[key] = val

            elif val is None:

                newdict[key] = 'NULL'

            else:
                val =  "'" + val + "'"

                newdict[key] = val

        tmpstr =  "insert into AnalysisStatus(Name,Rank,Status) values(%s,%s,%s)"%(newdict['Pog'],newdict['Sog'],newdict['Log'])
        
        self.assertTrue(tmpstr == "insert into AnalysisStatus(Name,Rank,Status) values('Sog',NULL,2)")

if __name__ == "__main__":                           # And run the file
    unittest.main()   
