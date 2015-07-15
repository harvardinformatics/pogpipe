import os
import sys
import logging

from datetime                   import datetime

from sqlalchemy                 import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import relationship,backref

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
    working_dir    = Column(String(250), nullable=True)
    output_dir     = Column(String(250), nullable=True)

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
    
    def init(self):
        """ Function to set up any analysis specific variables """
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

    def getCommands(self):

        """Constructs and returns the command line to run"""


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
    output_string_type      = Column(String(250),  nullable=False)
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
