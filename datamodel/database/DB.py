import os
import sys

from datetime                   import datetime

from sqlalchemy                 import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import relationship,backref
from sqlalchemy                 import create_engine
from sqlalchemy.sql             import func 

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

    input_files = relationship("AnalysisInputFile", order_by="AnalysisInputFile.id", backref="analysis")

class AnalysisInputFile(Base):

    __tablename__ = 'analysis_input_file'

    id                 = Column(Integer,      primary_key=True)
    analysis_id        = Column(Integer,      ForeignKey('analysis.id'))
    input_file         = Column(String(250),  nullable=False)
    input_file_type    = Column(String(250),  nullable=False)
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

    analysis = relationship("Analysis",backref=backref('output_files', order_by=id))

class AnalysisExpectedOutputFile(Base):

    __tablename__ = 'analysis_expected_output_file'

    id                          = Column(Integer,      primary_key=True)
    analysis_id                 = Column(Integer,      ForeignKey('analysis.id'))
    expected_output_file        = Column(String(250),  nullable=False)
    expected_output_file_type   = Column(String(250),  nullable=False)
    expected_output_file_rank   = Column(Integer,      nullable=False)
    date_created                = Column(DateTime,     default=datetime.utcnow)


    analysis = relationship("Analysis",backref=backref('expected_output_files', order_by=id))

class AnalysisStatus(Base):

    __tablename__ = 'analysis_status'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    status                  = Column(String(250),  nullable=False)
    status_type             = Column(String(250),  nullable=False)
    status_rank             = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    analysis = relationship("Analysis",backref=backref('status', order_by=id))

class AnalysisCommand(Base):

    __tablename__ = 'analysis_command'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    command                 = Column(String(250),  nullable=False)
    command_type            = Column(String(250),  nullable=False)
    command_rank            = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    analysis = relationship("Analysis",backref=backref('commands', order_by=id))

class AnalysisOutputString(Base):

    __tablename__ = 'analysis_output_string'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    output_string           = Column(String(250),  nullable=False)
    output_string_type      = Column(String(250),  nullable=False)
    output_string_rank      = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    analysis = relationship("Analysis",backref=backref('output_strings', order_by=id))

class AnalysisSummaryValue(Base):

    __tablename__ = 'analysis_summary_value'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    summary_value_string    = Column(String(250),  nullable=False)
    summary_value_type      = Column(String(250),  nullable=False)
    summary_value_rank      = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    analysis = relationship("Analysis",backref=backref('summary_values', order_by=id))

class AnalysisSlurmValue(Base):

    __tablename__ = 'analysis_slurm_value'

    id                      = Column(Integer,      primary_key=True)
    analysis_id             = Column(Integer,      ForeignKey('analysis.id'))
    slurm_value_string      = Column(String(250),  nullable=False)
    slurm_value_type        = Column(String(250),  nullable=False)
    slurm_value_rank        = Column(Integer,      nullable=False)
    date_created            = Column(DateTime,     default=datetime.utcnow)

    analysis = relationship("Analysis",backref=backref('slurm_values', order_by=id))
#engine = create_engine('sqlite:///)
#engine.echo = True

#Base.metadata.create_all(engine)
