from argparse  import ArgumentParser
from config    import settings

import importlib
import logging
import os
import sys
import csv
import pprint

from datamodel.AnalysisRunnerWrapper import AnalysisRunnerWrapper

def main(args):

    logging.info(" ========> run_analysis for %20s %s"%(args.analysis,args.input))

    logging.info("ARGS %s"%args)

    arw = AnalysisRunnerWrapper(args);

    if args.launch:

        print "Getting %d %s jobs"%(args.launch,args.analysis)
        jobids = arw.fetchLaunchableJobIDs(args.launch,args.analysis)

        print "Jobids %s"%(jobids)

        for jobid in jobids:
            print "Job id %d"%jobid

            arw.createAnalysisRunnerClassFromID(jobid)
            arw.run()

        return

    if args.jobid:

        jobid = int(args.jobid)
        arw.createAnalysisRunnerClassFromID(jobid)

    else:

        arw.createAnalysisRunnerClass()

    if args.register is False:

        print "Running\n";
        arw.run()
    

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Run analysis module')

    parser.add_argument('-a','--analysis'   , help='Which analysis to run')
    parser.add_argument('-i','--input'      , help="List of input files separated by ,")
    parser.add_argument('-t','--input_type' , help="List of input types separated by ,")
    parser.add_argument('-o','--outdir'     , help="Directory to put the output,")
    parser.add_argument('-r','--runtype'    , help="How to run the command [local,slurm],")
    parser.add_argument('-R','--register'   , help="Register new analysis in db but don't run",  action="store_true")
    parser.add_argument('-d','--dbname'     , help="Set the sqlite database name")
    parser.add_argument('-q','--queue'      , help="Slurm queue to submit to")
    parser.add_argument('-p','--param'      , help="Parameters to send to the command")
    parser.add_argument('-c','--cores'      , help="Number of cores to run on [1]",              type=int)
    parser.add_argument('-m','--mempercore' , help="Memory per core in Mb [1000]",               type=int)
    parser.add_argument('-l','--launch'     , help="Launch n jobs",                              type=int)
    parser.add_argument('-j','--jobid'      , help="Database analysis job id to run")
    
    args = parser.parse_args()

    # Parse the input string into an array of files

    if args.input:
        args.input = args.input.split(',')
    else:
        args.input = list()

    # Parse the input type string into an array of strings

    if args.input_type:
        args.input_type = args.input_type.split(',')
    else:
        args.input_type = list()

    if args.param:
        tmp1 = args.param.split(",");
        tmp2 = {}
        
        for tmp in tmp1:
            t = tmp.split("=")
            
            if len(t) == 1:
                tmp2[t] = True
            else:
                tmp2[t[0]] = t[1]

        args.param = tmp2

    main(args)

