import os
import sys
import shutil
import logging

from datetime                   import datetime

#from datamodel.database.DB import Analysis, AnalysisCommand, AnalysisExpectedOutputFile, AnalysisInputFile, AnalysisOutputFile
#from datamodel.database.DB import AnalysisOutputString, AnalysisSlurmValue, AnalysisStatus, AnalysisSummaryValue

from datamodel.FileUtils        import FileUtils
from config                     import settings
from datamodel.database.DB import AnalysisInputFile, AnalysisOutputString, AnalysisOutputFile, AnalysisExpectedOutputFile

class AnalysisUtils():

    @staticmethod        
    def checkDirectory(anaobj,directory,dirtype):
      
        if not directory:
            raise IOError("No [%s] directory set for analysis module [%s]"%(dirtype,anaobj.name))
 
        if not os.path.exists(directory):
            raise IOError("[%s] directory [%s] doesn't exist for analysis module [%s]"%(dirtype,directory,anaobj.name))
 
        if not os.path.isdir(directory):
            raise IOError("[%s] directory [%s] is not a directory in analysis module"%(dirtype,directory,anaobj.name))

        if not os.access(directory,os.W_OK):
            raise IOError("[%s] directory [%s] not writable for analysis module [%s]"%(dirtype,directory,anaobj.name))

    @staticmethod
    def checkInputFiles(anaobj):

        valid = True;

        for i in anaobj.input_files:

            if os.path.isfile(i.input_file) == False:
                valid = False

        logging.info(" ========> Analysis %20s called checkInputFiles:  Input Files Valid %s"%(anaobj.name,valid))

        return valid
    
    @staticmethod
    def checkDiskSpace(anaobj):
        
        print anaobj.currentstatus
        print anaobj.working_dir
        
        bytes = FileUtils.getFreeDiskSpace(anaobj.working_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(anaobj.name,anaobj.working_dir,bytes,anaobj.minimum_space_needed))

        if anaobj.minimum_space_needed and bytes < anaobj.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(anaobj.working_dir,anaobj.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(anaobj.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(anaobj.working_dir,anaobj.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(anaobj.name,str))
            raise Exception(str)


        bytes = FileUtils.getFreeDiskSpace(anaobj.output_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(anaobj.name,anaobj.output_dir,bytes,anaobj.minimum_space_needed))

        if anaobj.minimum_space_needed and bytes < anaobj.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(anaobj.output_dir,anaobj.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(anaobj.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(anaobj.output_dir,anaobj.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(anaobj.name,str))
            raise Exception(str)
    @staticmethod
    def addOutputString(anaobj,tmpstr):
        anaobj.output_strings.append(AnalysisOutputString(output_string=tmpstr,output_string_rank=len(anaobj.output_strings)+1))
        
    @staticmethod
    def addOutputFile(anaobj,tmpstr):
        anaobj.output_files.append(AnalysisOutputFile(output_file=tmpstr,output_file_rank=len(anaobj.output_files)+1))
        
    @staticmethod
    def addExpectedOutputFile(anaobj,tmpstr):
        anaobj.expected_output_files.append(AnalysisExpectedOutputFile(expected_output_file=tmpstr,expected_output_file_rank=len(anaobj.expected_output_files)+1))
        
    @staticmethod   
    def getOutputStrings(anaobj):
        return map(lambda x:x.output_string,anaobj.output_strings)

    @staticmethod   
    def getInputFiles(anaobj):
        return map(lambda x:x.input_file,anaobj.input_files)
    
    @staticmethod
    def setInputFiles(anaobj,input_files,input_types):
        anaobj.input_files = []
                
        for i,val in enumerate(input_files):
            tmptype = None
            if i in input_types:
                tmptype = input_types[i]
                
            tmpf = AnalysisInputFile(input_file=val,input_file_rank=i+1,input_file_type=tmptype)
            anaobj.input_files.append(tmpf)
        
        
        logging.info("SUCCESS Setting input files and types in analysis module [%s]. Files are [%s]"%(anaobj.name,", ".join(map(lambda x:x.input_file,anaobj.input_files))))
        return True
    
    @staticmethod
    def postProcessOutput(anaobj):
        """ Checks expected output files exist in the working directory and copies them over to the output directory """

        logging.info(" ========> Analysis %20s called postProcessOutput:"%(anaobj.name))

        if AnalysisUtils.checkExpectedOutputFiles(anaobj) == False:
            raise Exception("Missing expected output files. Number missing are [%d]"%(len(anaobj.missing_output_files)))

        FileUtils.checkDirExists(anaobj.output_dir)

        tmpfiles = []

        logging.info(" ========> Analysis %20s called postProcessOutput: Moving files from %s to %s "%(anaobj.name,anaobj.working_dir,anaobj.output_dir))
        try:
            for srcfileobj in anaobj.expected_output_files:
                srcfile     = srcfileobj.expected_output_file
                
                fullsrcfile = os.path.join(anaobj.working_dir,srcfile)
                destfile    = os.path.join(anaobj.output_dir,srcfile)

                FileUtils.checkDirExistsForFile(destfile)

                res = shutil.move(fullsrcfile,destfile)

                if res == None:
                    res = "OK"
                else:
                    res = "FAILED"

                print "Checking %s"%destfile
                tmpfiles.append(destfile)
                
                logging.info(" ========> Analysis %20s called postProcessOutput: Result of file move for  %s = %s" % (anaobj.name,srcfile,res))

        except Exception as e:
            logging.info(" ========> Analysis %20s file move failed %s"%(anaobj.name,e))
            raise

        anaobj.output_files = []
        for i in tmpfiles:
            AnalysisUtils.addOutputFile(anaobj,i)

        for f in anaobj.temp_output_files:
            logging.info(" ========> Analysis %20s removing temp file %s "%(anaobj.name,f))
            res = os.remove(f) 

    @staticmethod
    def checkExpectedOutputFiles(anaobj):
            working_dir = anaobj.working_dir

            valid = True;

            missing_output_files = []
            found_output_files   = []

            for fobj in anaobj.expected_output_files:
                f = fobj.expected_output_file
            
                if os.path.isfile(os.path.join(working_dir,f)):
                    found_output_files.append(os.path.join(working_dir,f))
                else:
                    missing_output_files.append(os.path.join(working_dir,f))
                    valid = False

            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected count %s"%(anaobj.name,len(anaobj.expected_output_files)))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected valid %s"%(anaobj.name,valid))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing count  %s"%(anaobj.name,len(missing_output_files)))
            logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing files  %s"%(anaobj.name,", ".join(missing_output_files)))

            anaobj.missing_output_files = missing_output_files
            anaobj.found_output_files   = found_output_files

            return valid
