from datetime import datetime

import logging

POGPIPEROOT          = '/Users/mclamp/git/harvardinformatics/pogpipe/'
#POGPIPEROOT          = '/home/mclamp/git/pogpipe/'
#POGPIPEROOT          = '/n/home_rc/mclamp/git/bitbucket/PogPipe/'

OSNAME               = "macosx"
#OSNAME               = "centos6"

TOOLDIR              = POGPIPEROOT + "tools/" + OSNAME + "/"
DBNAME               = POGPIPEROOT + "pogpipe.db"

OUTPUT_DIR           = '/Users/mclamp/git/harvardinformatics/pogpipe/testout/'
WORKING_DIR          = POGPIPEROOT + "working_dir/"
#OUTPUT_DIR           = '/n/regal/informatics/PogPipe/testout/'
#OUTPUT_DIR           = '/home/mclamp/git/pogpipe/testout/'

LOGFILE              = '/tmp/pogpipe_' + datetime.now().strftime("%Y-%m-%d")+'.log'
TMPDIR               = '/tmp/'
TESTDBNAME           = 'test.db'
TESTLOGFILE          = 'test.log'

ANALYSIS_MODULES     = ['FastQC','DirectoryList','DirectorySize','Bowtie2','BlastOutput6Parser','BlastDB']

#DATABASE_DIR         = ['/cygdrive/c/Users/mclamp/Dropbox/databases/']
#DATABASE_DIR         = ['/n/home_rc/mclamp/Dropbox/databases/']
#DATABASE_DIR         = ['/n/regal/informatics/databases/']

ENGINE                = None

logging.basicConfig(filename=LOGFILE,level=logging.INFO)

