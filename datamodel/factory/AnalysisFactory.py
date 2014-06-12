import os
import sys
import os.path
import logging
import importlib

from   config          import settings

class AnalysisFactory(object):
    """Factory class that creates different types of Analysis object"""

    @staticmethod
    def createAnalysisFromModuleName(modulename):
        
        modules    = settings.ANALYSIS_MODULES
        moduleset  = set(modules)
    
        if modulename in moduleset:
            logging.info("  Found module %s" % modulename)
        else:
            logging.info("  Can't find module %s" % modulename)

        analysisname = "datamodel." + modulename + "Analysis"

        logging.info("analysis name is " + analysisname)

        module   = importlib.import_module(analysisname)
        modclass = getattr(module,modulename + "Analysis")

        return modclass()

    @staticmethod
    def toString(ana):

        str = ""
        
        str += "%-20s %-20s\n" % ("id",              ana.id)
        str += "%-20s %-20s\n" % ("name",            ana.name)
        str += "%-20s %-20s\n" % ("owner",           ana.owner)
        str += "%-20s %-20s\n" % ("owner_email",     ana.owner_email)
        str += "%-20s %-20s\n" % ("current_status",  ana.current_status)
        str += "%-20s %-20s\n" % ("output_status",   ana.output_status)


        str += "%-20s %-20s\n" % ("runtype",   ana.runtype)
        str += "%-20s %-20s\n" % ("param",     ana.param)
        str += "%-20s %-20s\n" % ("queue",     ana.queue)
        str += "%-20s %-20s\n" % ("slurmid",   ana.slurmid)
        str += "%-20s %-20s\n" % ("cores",     ana.cores)
        str += "%-20s %-20s\n" % ("mempercore",ana.mempercore)

        str += "%-20s %-20s\n" % ("output_status",  ana.output_status)

        str += "%-20s %-20s\n" % ("input_dir",        ana.input_dir)
        str += "%-20s %-20s\n" % ("working_dir",      ana.working_dir)
        str += "%-20s %-20s\n" % ("output_dir",       ana.output_dir)

        str += "\n"

        str += "   -  Input Files: %d\n"             % len(ana.input_files)

        for f in ana.input_files:
            str += "       - %s\n" % f

        str += "\n"

        str += "   -  Input types: %d\n"             % len(ana.input_types)

        for f in ana.input_types:
            str += "       - %s\n" % f

        str += "\n"

        str += "   -  Output files: %d\n"            % len(ana.output_files)

        for f in ana.output_files:
            str += "       - %s\n" % f

        str += "\n"

        str += "   -  Output types: %d\n"            % len(ana.output_types)

        for f in ana.output_types:
            str += "       - %s\n" % f

        str += "\n"

        str += "   -  Expected output files: %d\n"   % len(ana.expected_output_files)

        for f in ana.expected_output_files:
            str += "       - %s\n" % f


        str += "\n"
        str += "   -  Commands: %d\n" % len(ana.commands)

        for f in ana.commands:
            str += "       - Command  %s\n" % f

        str += "\n"
        str += "   -  Output Strings: %d\n" % len(ana.output_str)

        for f in ana.output_str:
            str += "       - %s\n" % f

        str += "\n"
        str += "   -  Summary Data: %d\n" % len(ana.summary_data)

        for key,value in ana.summary_data.iteritems():
            str + "Summary Data %20s %20s\n" % (key,value)

        return str
    

