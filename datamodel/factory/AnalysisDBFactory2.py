import os
import sys
import logging
import sqlite3

from   config             import settings
from   datamodel.Analysis import Analysis

class AnalysisDBFactory(object):

    """Factory class that creates different types of Analysis object"""

    tablelist = ['Analysis','AnalysisInput','AnalysisOutput','AnalysisCommand','AnalysisStatus','AnalysisSummaryData']

    def __init__(self,dbname):

        self.connect(dbname)
        
        tables = self.getTables()

        if len(tables) == 0:
            self.createAnalysisTables()


    def connect(self,dbname):
        self.dbname = dbname

        try:
            con = sqlite3.connect(dbname)
            
            cur = con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
    
            data = cur.fetchone()
    
            print "SQLite version: %s" % data                
    
        except sqlite3.Error, e:
            
            print "Error %s:" % e.args[0]
    
        self.con = con


    def getTables(self):
        try:

            with self.con:

                cur = self.executeQuery('SELECT name FROM sqlite_master WHERE type = "table"')

                rows    = cur.fetchall()

                return rows

        except sqlite3.Error, e:
    
            print "Error %s:" % e.args[0]
            return False

        return True


    def createAnalysisTables(self):

        try:

            with self.con:
    
                cur = self.executeQuery("DROP TABLE IF EXISTS Analysis")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisInputFile")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisStatus")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisCommand")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisOutputFile")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisSummaryValue")
                
                self.createAnalysisTable()                     # Stores general info about the analysis job
                
                self.createAnalysisLinkedTable("InputFile")    # Stores the input files and types
                self.createAnalysisLinkedTable("OutputFile")   # Stores the output files and types
                self.createAnalysisLinkedTable("SummaryValue") # Stores the key/value data pairs that summarize the output from the job
                self.createAnalysisLinkedTable("OutputString") # Stores the stdout from the commands
                self.createAnalysisLinkedTable("Command")      # Stores the commands that are run
                self.createAnalysisLinkedTable("Status")       # Stores the status and timestamps as the job progresses

        except sqlite3.Error, e:
    
            if self.con:
                self.con.rollback()
        
                print "Error %s:" % e.args[0]
                return False

        return True

    def convstr(self,tmpstr):

        if tmpstr is None:
            return tmpstr
        elif isinstance(tmpstr,int):
            return tmpstr
        else:
            return "'"+tmpstr+"'"


    def saveAnalysis(self,anaobj):

        """ Save Analysis Object """

        with self.con:
            
            cur = self.con.cursor()    

            data = {}
            
            id            = self.convstr(anaobj.id)
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

            
            if id == None:                    # This is a new analysis
    
                sql = "insert into Analysis(Name,Owner,OwnerEmail,CurrentStatus,OutputStatus,InputDir,WorkingDir,OutputDir,RunType,Param,Queue,SlurmId,Cores,MemPerCore,DateCreated) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,%s)" %  (name,owner,owner_email,current_status,output_status,input_dir,working_dir,output_dir,runtype,param,queue,slurmid,cores,mempercore,date_created)
                
                cur = self.executeQuery(sql)
                
                id = cur.lastrowid
                
                anaobj.id = id
                
                logging.info("ID is %s" % id)


            else:                            # This is an updated analysis

                sql = "update Analysis set Name='%s', Owner='%s', OwnerEmail='%s', CurrentStatus='%s', OutputStatus='%s', InputDir='%s', WorkingDir='%s', OutputDir='%s', RunType='%s',Param='%s',Queue='%s',SlurmId=%d,Cores=%d, MemPerCore=%d  where ID = %d" %   (name,owner,owner_email,current_status,output_status,input_dir,working_dir,output_dir,runtype,param,queue,slurmid,cores,mempercore,id)
                
                cur = self.executeQuery(sql)


                # Now delete from the other tables before inserting afresh (leave the status table as we want to keep these)
       
                linkedtables = ["InputFile","OutputFile","Command","SummaryValue","OutputString"]

                for t in linkedtables:
                    sql = "delete from Analysis"+t+" where AnalysisId = %d" % id
                    cur = self.executeQuery(sql)

                
            """ Now save the rest of the data to the other tables """

            self.saveAnalysisLinkedTable("InputFile",id,input_files,input_types)
            self.saveAnalysisLinkedTable("OutputFile",id,output_files,output_types)
            self.saveAnalysisLinkedTable("Command",id,commands,None)
            self.saveAnalysisLinkedTable("OutputString",id,output_str,None)
            print summary_data
            self.saveAnalysisLinkedTable("SummaryValue",id,summary_data,summary_data.keys())
            
            """ Save the status """
                
            
            sql = "insert into AnalysisStatus(AnalysisID,Status) values(%d,'%s')" % (id,anaobj.current_status)

            cur.execute(sql)
        

    def fetchAnalysisByID(self,id):

        try:
            sql = "select * from Analysis where ID = %d" % id

            cur = self.executeQuery(sql)
        
            rows = cur.fetchall()

            if (len(rows) == 1):

                row  = rows[0]
                name = row[1]

                ana = Analysis(name)

                ana.id            = id

                ana.owner         = row[2]
                ana.owner_email   = row[3]
                ana.current_status= row[4]
                ana.output_status = row[5]
                ana.input_dir     = row[6]
                ana.workding_dir  = row[7]
                ana.output_dir    = row[8]
                ana.runtype       = row[9]
                ana.param         = row[9]
                ana.queue         = row[10]
                ana.slurmid       = row[11]
                ana.cores         = row[12]
                ana.mempercore    = row[13]
                ana.date_created  = row[14]

                """ Get the data from the linked tables """

                tables = ['InputFile','OutputFile','Command','SummaryValue','Status']
                
                for t in tables:
                    
                    tmpstr = "Analysis"+t
                    cur = self.executeQuery("select * from %s where AnalysisID=%d" % (tmpstr,id))
                    rows = cur.fetchall()

                    for r in rows:
                        if t == "Input":
                            ana.input_files.append(r[2])
                            ana.input_types.append(r[3])
                        elif t == "Output":
                            ana.output_files.append(r[2])
                            ana.output_types.append(r[3])
                        elif t == "Cammand":
                            ana.commands.append(r[2])
                        elif t == "SummaryValue":
                            ana.summary_data.append(r[2])



            elif (len(rows) == 0):
                return None

            elif len(rows) > 1:
                print "ERROR: analysis id should be unique - multiple rows returned. id is [%d]" % id
                sys.exit(1)


            return ana

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error("Error %s:" % e.args[0])
                print "Error %s" % e.args[0]
                print "SQL is %s" % sql
                return cur

    def updateAnalysisStatus(self,ana,status):
        ana.status = status
        
        id = ana.id

        if id == None:
            raise Exception("ERROR: Can't update analysis that isn't in the database")

        try:

            cur = self.executeQuery("update Analysis set CurrentStatus='%s' where ID=%d" % (status,id))

            cur = self.executeQuery("insert into AnalysisStatus(AnalysisID,Status) values(%d,'%s')" % (id,status))

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error("Error %s:" % e.args[0])
                print "Error %s" % e.args[0]
                print "SQL is %s" % sql
                return cur


    def saveAnalysisLinkedTable(self,name,id,data,types):

        rank = 1
        i    = 0

        for dat in data:
            dattype = None

            if types and len(types) > i:
                dattype = types[i]
                
            sql = "insert into Analysis"+name+"(AnalysisID,"+name+","+name+"Type,"+name+"Rank) values(%d,'%s','%s',%d)" % (id,dat,dattype,rank)
                
            cur = self.executeQuery(sql)
                
            id = cur.lastrowid
                
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
        
    def executeQuery(self,sql):
        try:
            cur = self.con.cursor()
            
            logging.info("SQL: %s" % sql)
            
            cur.execute(sql)

            return cur
            
        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error("Error %s:" % e.args[0])
                print "Error %s" % e.args[0]
                print "SQL is %s" % sql
                return cur
