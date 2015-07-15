import os
import sys
import time
import logging
import sqlite3

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from   datetime                            import datetime
from   config                              import settings
from   argparse                            import ArgumentParser
from   datamodel.factory.AnalysisDBFactory import AnalysisDBFactory

class AnalysisDBWatcher(object):

    """ Class that watches the analysis database and spits out summary tables"""

    dbname = None
    dbobj  = None

    def __init__(self,dbname):

        self.setDBName(dbname)

    def setDBName(self,dbname):
        self.dbname = dbname
        self.dbobj  = AnalysisDBFactory(dbname)

    def getAnalysisSummary(self,analysis_type):

        if analysis_type:
            sql = "select count(*),CurrentStatus,Name from Analysis where Name='"+analysis_type+"' group by Name, CurrentStatus"
        else:
            sql = "select count(*),CurrentStatus,Name from Analysis group by Name, CurrentStatus"

        cur = self.dbobj.executeQuery(sql)

        rows = cur.fetchall()

        return rows

    def getAnalysisList(self,analysis_type):

        sql = "select ID,Name, CurrentStatus, DateCreated from Analysis where Name='"+analysis_type+"' order by DateCreated desc"

        cur = self.dbobj.executeQuery(sql)

        rows = cur.fetchall()

        return rows

if __name__ == "__main__":                           # And run the file
    watcher = AnalysisDBWatcher(settings.DBNAME)

    parser        = ArgumentParser(description = 'Module that watches an analysis db')

    parser.add_argument('-s','--status'         , help="Show summary status of all entries", action="store_true")
    parser.add_argument('-a','--analysis'       , help="Only show values for analysis type <analysis>")
    parser.add_argument('-j','--jobid'          , help="Show details of specified analysis job")
    parser.add_argument('-c','--current_status' , help="Show all jobs with specified current status")
    parser.add_argument('-l','--loop_time'      , help="Repeat the operation every <loop_time> seconds")

    args = parser.parse_args()

    print args
    status = True

    while status == True:

        dt   = datetime.now().strftime("%Y-%m-%d %H:%m:%S")

        if args.status:

            rows = watcher.getAnalysisSummary(args.analysis)

            print "Status at %s\n" % dt

            print "%20s %20s %5s"%("Analysis","Status","Count")
        
            for r in rows:
                print "%20s %20s %5d" % (r[2],r[1],r[0])
                
                print "\n"


        elif args.jobid:
            
            ana = watcher.dbobj.fetchAnalysisByID(int(args.jobid))

            print ana.toString()

        elif args.analysis:

            rows = watcher.getAnalysisList(args.analysis)

            print "%s Analysis entries at %s\n" % (args.analysis,dt)

            print "%10s %20s %20s %25s"%("ID","Name","CurrentStatus","DateCreated")
        
            for r in rows:
                print "%10s %20s %20s %25s" % (r[0],r[1],r[2],r[3])

        if args.loop_time:
            time.sleep(int(args.loop_time)*1.0)
        else:
            status = False


        

        
