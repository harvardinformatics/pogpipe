import re
import os
import sys
import logging
import sqlite3

from   datetime                          import datetime
from   config                            import settings
from   datamodel.Analysis                import Analysis
from   datamodel.factory.AnalysisFactory import AnalysisFactory

"""Factory class that creates/saves Analysis objects """

class AnalysisDBFactory(object):

    tablelist = ['Analysis','AnalysisInput','AnalysisOutput','AnalysisCommand','AnalysisStatus','AnalysisSummaryData','AnalsyisOutputString']

    """ Connect to the database, fetch the tables and create them if none exist  """

    def __init__(self,dbname):

        self.connect(dbname)
        
        tables = self.getTables()

        if len(tables) == 0:
            self.createAnalysisTables()
            
    """  Create all the analysis tables  """

    def createAnalysisTables(self):

        try:

            with self.con:
    
                cur = self.executeQuery("DROP TABLE IF EXISTS Analysis")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisInputFile")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisStatus")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisCommand")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisOutputFile")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisExpectedOutputFile")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisSlurmValue")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisSummaryValue")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisOutputString")
                
                self.createAnalysisTable()                             # Stores general info about the analysis job
                
                self.createAnalysisLinkedTable("InputFile")            # Stores the input files and types
                self.createAnalysisLinkedTable("OutputFile")           # Stores the output files and types
                self.createAnalysisLinkedTable("ExpectedOutputFile")   # Stores the expected output files and types
                self.createAnalysisLinkedTable("SlurmValue")           # Stores the slurm key value pairs
                self.createAnalysisLinkedTable("SummaryValue")         # Stores the key/value data pairs that summarize the output from the job
                self.createAnalysisLinkedTable("OutputString")         # Stores the stdout from the commands
                self.createAnalysisLinkedTable("Command")              # Stores the commands that are run
                self.createAnalysisLinkedTable("Status")               # Stores the status and timestamps as the job progresses

        except sqlite3.Error, e:
    
            if self.con:
                self.con.rollback()
        
                raise Exception("Error creating the analysis tables [%s]"%e.args[0])

        return True



    """ Save Analysis Object """

    def saveAnalysis(self,anaobj):
        logging.info(" ========> AnalysisDB Saving analysis : %s ID %s : Status : %s" % (anaobj.name,anaobj.id,anaobj.current_status))

        with self.con:
            
            cur = self.con.cursor()    

            data = {}
            
            id            = self.convstr(anaobj.id)                   # The convstr function puts quotes round strings, converts None to 'NULL' and leaves ints alone
            name          = self.convstr(anaobj.name)

            owner         = self.convstr(anaobj.owner)
            owner_email   = self.convstr(anaobj.owner_email)
            
            current_status= self.convstr(anaobj.current_status)
            output_status = self.convstr(anaobj.output_status)

            input_files   = self.convstr(anaobj.input_files)
            input_types   = self.convstr(anaobj.input_types)

            input_dir     = self.convstr(anaobj.input_dir)
            working_dir   = self.convstr(anaobj.working_dir)
            output_dir    = self.convstr(anaobj.output_dir)

            output_files  = self.convstr(anaobj.output_files)
            output_types  = self.convstr(anaobj.output_types)

            expected_output_files = self.convstr(anaobj.expected_output_files)

            commands      = self.convstr(anaobj.commands)
            output_str    = self.convstr(anaobj.output_str)
            summary_data  = self.convstr(anaobj.summary_data)

            runtype       = self.convstr(anaobj.runtype)
            param         = self.convstr(anaobj.param)

            queue         = self.convstr(anaobj.queue)
            slurmid       = self.convstr(anaobj.slurmid)
            cores         = self.convstr(anaobj.cores)
            mempercore    = self.convstr(anaobj.mempercore)

            date_created  = self.convstr(anaobj.date_created)
            
            slurm_data    = self.convstr(anaobj.slurmparams)

            if id == "NULL":                                    # This is a new analysis
                
                anaobj.date_created = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
                anaobj.last_updated = anaobj.date_created
                
                sql = "insert into Analysis(Name,Owner,OwnerEmail,CurrentStatus,OutputStatus,InputDir,WorkingDir,OutputDir,RunType,Param,Queue,SlurmId,Cores,MemPerCore,LastUpdated,DateCreated) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,'%s','%s')" %  (name,owner,owner_email,current_status,output_status,input_dir,working_dir,output_dir,runtype,param,queue,slurmid,cores,mempercore,anaobj.date_created,anaobj.date_created)
                
                cur = self.executeQuery(sql)
                
                id = cur.lastrowid
                
                anaobj.id = id                                  # Set the Analysis ID
                
            
            else:                                               # This is an updated analysis

                anaobj.last_updated = datetime.now().strftime("%Y-%m-%d %H:%m:%S")

                sql = "update Analysis set Name=%s, Owner=%s, OwnerEmail=%s, CurrentStatus=%s, OutputStatus=%s, InputDir=%s, WorkingDir=%s, OutputDir=%s, RunType=%s,Param=%s,Queue=%s,SlurmId=%d,Cores=%d, MemPerCore=%d, LastUpdated='%s'  where ID = %s" %   (name,owner,owner_email,current_status,output_status,input_dir,working_dir,output_dir,runtype,param,queue,slurmid,cores,mempercore,anaobj.last_updated,id)
                
                cur = self.executeQuery(sql)

                # Now delete from the other tables before inserting afresh (leave the status table as we want to keep these)
       
                linkedtables = ["InputFile","ExpectedOutputFile","OutputFile","Command","SlurmValue","SummaryValue","OutputString"]

                for t in linkedtables:
                    sql = "delete from Analysis"+t+" where AnalysisId = %s" % id
                    cur = self.executeQuery(sql)

                
            # Now save the rest of the data to the other tables

            print "OUTPUT FILES %s"%output_files
            self.saveAnalysisLinkedTable("InputFile",    id,input_files, input_types)
            self.saveAnalysisLinkedTable("ExpectedOutputFile",   id,expected_output_files,output_types)
            self.saveAnalysisLinkedTable("OutputFile",   id,output_files,output_types)
            self.saveAnalysisLinkedTable("OutputString", id,output_str,  None)
            self.saveAnalysisLinkedTable("Command",      id,commands,    None)
            self.saveAnalysisLinkedTable("SlurmValue",  id,anaobj.slurmparams,    None)
            self.saveAnalysisLinkedTable("SummaryValue", id,summary_data,summary_data.keys())
            
            # Save the status
            
            sql = "insert into AnalysisStatus(AnalysisID,Status) values(%s,'%s')" % (id,anaobj.current_status)

            cur.execute(sql)

            self.con.commit()
 
            return True

    def existsAnalysisID(self,id):

        cur = self.executeQuery("select * from Analysis where ID = %s"%id)

        rows = cur.fetchall()

        if len(rows) == 1:
            return True
        elif len(rows) > 1:
            raise Exception("More than one analysis row exists for id %s"%id)
        else:
            return False

            
    def fetchLaunchableJobIDs(self,numjobs,analysis):

        logging.info(" ========> AnalysisDB Fetching launchable jobids : %d %s" % (numjobs,analysis))

        try:

            if analysis:

                sql = "select ID from Analysis where CurrentStatus = 'NEW' and Name = '%s' order by DateCreated limit %d"%(analysis,numjobs)

            else:

                sql = "select ID from Analysis where CurrentStatus = 'NEW' order by DateCreated limit %d"%(numjobs)


            cur = self.executeQuery(sql)
        
            rows = cur.fetchall()

            jobids = []

            for r in rows:
                
                jobids.append(int(r[0]))

            return jobids

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error(" ========> AnalysisDB Error fetching %d %s analysis jobs : %s"%(numjobs,analysis,e.args[0]))
                
                raise 


    def fetchAnalysisByID(self,id):

        logging.info(" ========> AnalysisDB Fetching analysis by id : %s" % id)

        try:
            sql = "select * from Analysis where ID = %s" % id

            cur = self.executeQuery(sql)
        
            rows = cur.fetchall()

            if (len(rows) == 1):

                row  = rows[0]
                name = row[1]

                ana = AnalysisFactory.createAnalysisFromModuleName(name)

                ana.id            = id

                ana.owner         = row[2]
                ana.owner_email   = row[3]
                ana.current_status= row[4]
                ana.output_status = row[5]
                ana.input_dir     = row[6]
                ana.working_dir   = row[7]
                ana.output_dir    = row[8]
                ana.runtype       = row[9]
                ana.param         = row[10]
                ana.queue         = row[11]
                ana.slurmid       = row[12]
                ana.cores         = row[13]
                ana.mempercore    = row[14]
                ana.last_updated  = row[15]
                ana.date_created  = row[16]

                # Get the data from the linked tables

                tables = ['InputFile','ExpectedOutputFile','OutputFile','Command','SlurmValue','SummaryValue','Status']
                
                for t in tables:
                    
                    tmpstr = "Analysis"+t
                    query  = "select * from %s where AnalysisID=%d" % (tmpstr,id)

                    cur  = self.executeQuery(query)
                    rows = cur.fetchall()

                    for r in rows:

                        if t == "Command":

                            ana.commands.append(r[2])

                        if t == "InputFile":

                            ana.input_files.append(r[2])
                            ana.input_types.append(r[3])
                            
                        if t == "ExpectedOutputFile":

                            ana.expected_output_files.append(r[2])

                        if t == "OutputFile":

                            ana.output_files.append(r[2])
                            ana.output_types.append(r[3])
                            

                        if t == "SlurmValue":

                            ana.slurmparams[r[2]] = r[3]

                        if t == "SummaryValue":

                            ana.summary_data[r[2]] = r[3]

            elif (len(rows) == 0):
                return None

            elif len(rows) > 1:
                logging.error(" ========> AnalysisDB Error fetching analysis. Non unique id %d : %s"%(id,e.args[0]))
                raise Exception("ERROR: analysis id should be unique - multiple rows returned. id is [%d]" % id)


            ana.init()

            print ana.toString()

            return ana

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error(" ========> AnalysisDB Error fetching analysis id %d : %s"%(id,e.args[0]))
                
                raise

    def updateAnalysisStatus(self,ana,status):
        logging.info(" ========> AnalysisDB Updating analysis status id : %s status %s" % (ana.id,status))

        ana.current_status = status
        
        id = ana.id

        if id == None:
            raise Exception("ERROR: Can't update analysis that isn't in the database")

        try:
            dt =  datetime.now().strftime("%Y-%m-%d %H:%m:%S")

            query1 = "update Analysis set CurrentStatus='%s',LastUpdated='%s'  where ID=%s"            % (status,dt,id)
            query2 = "insert into AnalysisStatus(AnalysisID,Status) values(%s,'%s')" % (id,status)

            cur = self.executeQuery(query1)
            cur = self.executeQuery(query2)

            self.con.commit()

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                raise

    """ 

    Helper function to save data to one of the tables linked to analysis (InputFile,OutputFile,Command,Status,OutputString,SummaryValue)

    """

    def saveAnalysisLinkedTable(self,name,id,data,types):

        rank = 1
        i    = 0

        if name == "SummaryValue" or name == "SlurmValue":

            for key,value in data.iteritems():
                key   = self.convstr(key)

                sql = "insert into Analysis"+name+"(AnalysisID,"+name+","+name+"Type,"+name+"Rank) values(%s,%s,%s,%d)" % (id,value,key,rank)

                cur = self.executeQuery(sql)
                self.con.commit()

                rank = rank + 1
        else:
            for dat in data:

                # Set the type to NULL if we don't have a types array

                dattype = "NULL"
                tmpdat  = dat

                if types and len(types) > i:
                    dattype = types[i]

                sql = "insert into Analysis"+name+"(AnalysisID,"+name+","+name+"Type,"+name+"Rank) values(%s,%s,%s,%d)" % (id,tmpdat,dattype,rank)
            
                cur = self.executeQuery(sql)
                self.con.commit()

                rank = rank + 1
                i    = i    + 1


    """

    SQL to create the main analysis table and the linked tables

    """

    def createAnalysisTable(self):

        tmpstr = """CREATE TABLE Analysis(ID            INTEGER primary key,
                                          Name          TEXT, 
                                          Owner         TEXT,
                                          OwnerEmail    TEXT,
                         
                                          CurrentStatus TEXT default "NEW",
                                          OutputStatus  TEXT,
                                          
                                          InputDir      TEXT,
                                          WorkingDir    TEXT,
                                          OutputDir     TEXT,

                                          RunType       TEXT,
                                          Param         TEXT,

                                          Queue         TEXT,
                                          SlurmId       INT,
                                          Cores         INT, 
                                          MemPerCore    INT,

                                          LastUpdated   DATETIME default current_timestamp,
                                          DateCreated   DATETIME default current_timestamp)"""

        cur = self.executeQuery(tmpstr.strip('\n'))

                      
    def createAnalysisLinkedTable(self,name):
        tmpstr = """CREATE TABLE Analysis"""+name+"""(  ID          INTEGER primary key,
                                                       AnalysisID  INT,
                                                       """+name+"""       TEXT,
                                                       """+name+"""Type   TEXT,
                                                       """+name+"""Rank   INT,
                                                       DateCreated DATETIME default current_timestamp)"""

        cur = self.executeQuery(tmpstr.strip('\n'))


    """

    Utility function to execute some sql and rollback with an error if it fails.
    It returns a cursor so rows can be retrieved.


    """
        
    def executeQuery(self,sql):
        logging.info(" ========> AnalysisDBSQL Query string %s"%(sql))

        try:
            cur = self.con.cursor()
            cur.execute(sql)

            return cur
            
        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                raise

    """ 

    This utility function is to convert None into 'NULL' strings into 'mysql' and leave ints alone 

    """

    def convstr(self,tmpstr):

        if isinstance(tmpstr,dict):

            newstr = {}

            for key,val in tmpstr.iteritems():

                if val is None:
                  newstr[key] = "NULL"
                elif isinstance(val,int):
                    newstr[key] = val
                else:
                    newstr[key] = "'"+val+"'"

            return newstr

        elif isinstance(tmpstr,list):

            newstr = []

            for i,t in enumerate(tmpstr):
                if t is None:
                    newstr.append('NULL')
                elif isinstance(t,int):
                    newstr.append(t)
                else:
                    newstr.append("'"+t+"'")

            return newstr

        else:
            if tmpstr is None:
                return "NULL"
            elif isinstance(tmpstr,int):
                return tmpstr
            else:
                return "'"+tmpstr+"'"


    """

    Connect to the db and fetch the sqlite version

    """

    def connect(self,dbname):
        self.dbname = dbname

        try:
            con = sqlite3.connect(dbname)
            
            cur = con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
    
            data = cur.fetchone()
    
            logging.info(" ========> AnalysisDBSQL SQLite version %s" % data)
    
        except sqlite3.Error, e:
            
            
            raise
    
        self.con = con

    """

    Fetch all tables in the DB

    """

    def getTables(self):
        try:

            with self.con:

                cur = self.executeQuery('SELECT name FROM sqlite_master WHERE type = "table"')

                rows    = cur.fetchall()

                return rows

        except sqlite3.Error, e:
    
            print "Error %s:" % e.args[0]
            raise Exception("Error executing sql %s" % e.args[0])

        return True

