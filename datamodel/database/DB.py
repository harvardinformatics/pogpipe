import os
import sys
import shutil
import logging

from datetime                   import datetime

from sqlalchemy                 import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import relationship,backref

from datamodel.FileUtils        import FileUtils

from config import settings

Base = declarative_base()

class Analysis(Base):

    __tablename__ = 'analysis'

    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.

    id             = Column(Integer,     primary_key=True)
    name           = Column(String(250), nullable=False)
    owner          = Column(String(250), nullable=True)
    owneremail     = Column(String(250), nullable=True)
     
    currentstatus  = Column(String(250), nullable=False,default="NEW")
    outputstatus   = Column(String(250), nullable=True)

    input_dir      = Column(String(250), nullable=True)
    working_dir    = Column(String(250), nullable=True, default=settings.WORKING_DIR)
    output_dir     = Column(String(250), nullable=True, default=settings.OUTPUT_DIR)

    run_type       = Column(String(250), nullable=True)
    param          = Column(String(250), nullable=True)

    queue          = Column(String(250), nullable=True)
    slurmid        = Column(Integer,     nullable=True)
    cores          = Column(Integer,     nullable=True)
    mempercore     = Column(Integer,     nullable=True)

    date_created   = Column(DateTime,    default=datetime.utcnow)
    
    input_files    = relationship("AnalysisInputFile",       order_by="AnalysisInputFile.input_file_rank",           backref="analysis")
    output_files   = relationship("AnalysisOutputFile",      order_by="AnalysisOutputFile.output_file_rank",         backref="analysis")
    status         = relationship("AnalysisStatus",          order_by="AnalysisStatus.status_rank",                  backref="analysis")
    commands       = relationship("AnalysisCommand",         order_by="AnalysisCommand.command_rank",                backref="analysis")
    output_strings = relationship("AnalysisOutputString",    order_by="AnalysisOutputString.output_string_rank",     backref="analysis")
    summary_values = relationship("AnalysisSummaryValue",    order_by="AnalysisSummaryValue.summary_value_rank",     backref="analysis")
    slurm_values   = relationship("AnalysisSlurmValue",      order_by="AnalysisSlurmValue.slurm_value_rank",         backref="analysis")
    
    expected_output_files = relationship("AnalysisExpectedOutputFile", order_by="AnalysisExpectedOutputFile.expected_output_file_rank", backref="analysis")
    
    #def __init__(self,**kwargs):
    #    self._ensure_defaults()
    #    super(Base, self).__init__(**kwargs)
        
    def init(self):
        """ Function to set up any analysis specific variables """
        self._ensure_defaults()
        try:
            self.checkDirectory(self.output_dir,"output")
            self.checkDirectory(self.working_dir,"working")
        except Exception as e:
            logging.info("EXCEPTION checking directory in analysis module [%s]. Error is [%s]"%(self.name,e.message))
            raise
        
        logging.info("SUCCESS Checking output/workding directories in analysis module [%s]. Dirs are[%s][%s]"%(self.name,self.output_dir,self.working_dir))
        
    def checkDirectory(self,directory,dirtype):
      
        if not directory:
            raise IOError("No [%s] directory set for analysis module [%s]"%(dirtype,self.name))
 
        if not os.path.exists(directory):
            raise IOError("[%s] directory [%s] doesn't exist for analysis module [%s]"%(dirtype,directory,self.name))
 
        if not os.path.isdir(directory):
            raise IOError("[%s] directory [%s] is not a directory in analysis module"%(dirtype,directory,self.name))

        if not os.access(directory,os.W_OK):
            raise IOError("[%s] directory [%s] not writable for analysis module [%s]"%(dirtype,directory,self.name))

    def checkInputFiles(self):

        valid = True;

        for i in self.input_files:

            if os.path.isfile(i.input_file) == False:
                valid = False

        logging.info(" ========> Analysis %20s called checkInputFiles:  Input Files Valid %s"%(self.name,valid))

        return valid
    def checkDiskSpace(self):
        print self.currentstatus
        print self.working_dir
        bytes = FileUtils.getFreeDiskSpace(self.working_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(self.name,self.working_dir,bytes,self.minimum_space_needed))

        if self.minimum_space_needed and bytes < self.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.working_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.working_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)


        bytes = FileUtils.getFreeDiskSpace(self.output_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(self.name,self.output_dir,bytes,self.minimum_space_needed))

        if self.minimum_space_needed and bytes < self.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.output_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.output_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

    def getCommands(self):

        """Constructs and returns the command line to run"""

    def addOutputString(self,tmpstr):
        self.output_strings.append(AnalysisOutputString(output_string=tmpstr,output_string_rank=len(self.output_strings)+1))
    
    def addOutputFile(self,tmpstr):
        self.output_files.append(AnalysisOutputFile(output_file=tmpstr,output_file_rank=len(self.output_files)+1))
        
    def getOutputStrings(self):
        return map(lambda x:x.output_string,self.output_strings)
    
    def setInputFiles(self,input_files,input_types):
        self.input_files = []
                
        
        for i,val in enumerate(input_files):
            tmptype = None
            if i in input_types:
                tmptype = input_types[i]
                
            tmpf = AnalysisInputFile(input_file=val,input_file_rank=i+1,input_file_type=tmptype)
            self.input_files.append(tmpf)
        
        
        logging.info("SUCCESS Setting input files and types in analysis module [%s]. Files are [%s]"%(self.name,", ".join(map(lambda x:x.input_file,self.input_files))))
        return True
    
    def postProcessOutput(self):
        """ Checks expected output files exist in the working directory and copies them over to the output directory """

        logging.info(" ========> Analysis %20s called postProcessOutput:"%(self.name))

        if self.checkExpectedOutputFiles() == False:
            raise Exception("Missing expected output files. Number missing are [%d]"%(len(self.missing_output_files)))

        FileUtils.checkDirExists(self.output_dir)

        tmpfiles = []

        logging.info(" ========> Analysis %20s called postProcessOutput: Moving files from %s to %s "%(self.name,self.working_dir,self.output_dir))
        try:
            for srcfileobj in self.expected_output_files:
                srcfile     = srcfileobj.expected_output_file
                
                fullsrcfile = os.path.join(self.working_dir,srcfile)
                destfile    = os.path.join(self.output_dir,srcfile)

                FileUtils.checkDirExistsForFile(destfile)

                res = shutil.move(fullsrcfile,destfile)

                if res == None:
                    res = "OK"
                else:
                    res = "FAILED"

                print "Checking %s"%destfile
                tmpfiles.append(destfile)
                
                logging.info(" ========> Analysis %20s called postProcessOutput: Result of file move for  %s = %s" % (self.name,srcfile,res))

        except Exception as e:
            logging.info(" ========> Analysis %20s file move failed %s"%(self.name,e))
            raise

        self.output_files = []
        for i in tmpfiles:
            self.addOutputFile(i)

        for f in self.temp_output_files:
            logging.info(" ========> Analysis %20s removing temp file %s "%(self.name,f))
            res = os.remove(f) 

    def checkExpectedOutputFiles(self):
            working_dir = self.working_dir

            valid = True;

            missing_output_files = []
            found_output_files   = []

            for fobj in self.expected_output_files:
                f = fobj.expected_output_file
            
                if os.path.isfile(os.path.join(working_dir,f)):
                    found_output_files.append(os.path.join(working_dir,f))
                else:
                    missing_output_files.append(os.path.join(working_dir,f))
                    valid = False

            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected count %s"%(self.name,len(self.expected_output_files)))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected valid %s"%(self.name,valid))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing count  %s"%(self.name,len(missing_output_files)))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing files  %s"%(self.name,", ".join(missing_output_files)))

            self.missing_output_files = missing_output_files
            self.found_output_files   = found_output_files

            return valid

    def _ensure_defaults(self):
        for column in self.__table__.c:
            print column
            if getattr(self, column.name) is None and column.default is not None and column.default.is_scalar:
                setattr(self, column.name, column.default.arg)
                
class AnalysisInputFile(Base):

    __tablename__ = 'analysis_input_file'

    id                 = Column(Integer,      primary_key=True)
    analysis_id        = Column(Integer,      ForeignKey('analysis.id'))
    input_file         = Column(String(250),  nullable=False)
    input_file_type    = Column(String(250),  nullable=True)
    input_file_rank    = Column(Integer,      nullable=False)
    date_created       = Column(DateTime,     default=datetime.utcnow)
    
#    analysis = relationship("Analysis",backref=backref('input_files', order_by=id))

class AnalysisOutputFile(Base):

    __tablename__ = 'analysis_output_file'

    id                 = Column(Integer,      primary_key=True)
    analysis_id        = Column(Integer,      ForeignKey('analysis.id'))
    output_file        = Column(String(250),  nullable=False)
    output_file_type   = Column(String(250),  nullable=False)
    output_file_rank   = Column(Integer,      nullable=False)
    date_created       = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('output_files', order_by=id))

class AnalysisExpectedOutputFile(Base):

    __tablename__ = 'analysis_expected_output_file'

    id                          = Column(Integer,      primary_key=True)
    analysis_id                 = Column(Integer,      ForeignKey('analysis.id'))
    expected_output_file        = Column(String(250),  nullable=False)
    expected_output_file_type   = Column(String(250),  nullable=False)
    expected_output_file_rank   = Column(Integer,      nullable=False)
    date_created                = Column(DateTime,     default=datetime.utcnow)


    #analysis = relationship("Analysis",backref=backref('expected_output_files', order_by=id))

class AnalysisStatus(Base):

    __tablename__ = 'analysis_status'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    status                  = Column(String(250),  nullable=False)
    status_type             = Column(String(250),  nullable=False)
    status_rank             = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('status', order_by=id))

class AnalysisCommand(Base):

    __tablename__ = 'analysis_command'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    command                 = Column(String(250),  nullable=False)
    command_type            = Column(String(250),  nullable=False)
    command_rank            = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('commands', order_by=id))

class AnalysisOutputString(Base):

    __tablename__ = 'analysis_output_string'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    output_string           = Column(String(250),  nullable=False)
    output_string_type      = Column(String(250),  nullable=True)
    output_string_rank      = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('output_strings', order_by=id))

class AnalysisSummaryValue(Base):

    __tablename__ = 'analysis_summary_value'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    summary_value_string    = Column(String(250),  nullable=False)
    summary_value_type      = Column(String(250),  nullable=False)
    summary_value_rank      = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('summary_values', order_by=id))

class AnalysisSlurmValue(Base):

    __tablename__ = 'analysis_slurm_value'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    slurm_value_string      = Column(String(250),  nullable=False)
    slurm_value_type        = Column(String(250),  nullable=False)
    slurm_value_rank        = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    #analysis = relationship("Analysis",backref=backref('slurm_values', order_by=id))

def init_database():

    dbfile = settings.DBNAME

    settings.ENGINE = create_engine('sqlite:///'+dbfile)
    #settings.ENGINE.echo = True

    Base.metadata.create_all(settings.ENGINE)
