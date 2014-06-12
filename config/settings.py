from datetime import datetime

import logging

POGPIPEROOT          = '/Users/mclamp/git/bitbucket/PogPipe/'
#POGPIPEROOT          = '/n/home_rc/mclamp/git/bitbucket/PogPipe/'

OSNAME               = "macosx"
#OSNAME               = "centos6"
TOOLDIR              = POGPIPEROOT + "tools/" + OSNAME + "/"
DBNAME               = POGPIPEROOT + "pogpipe.db"
#OUTPUT_DIR           = '/n/regal/informatics/PogPipe/testout/'
OUTPUT_DIR           = '/Users/mclamp/git/bitbucket/PogPipe/testout/'

LOGFILE              = '/tmp/pogpipe_' + datetime.now().strftime("%Y-%m-%d")+'.log'
TMPDIR               = '/tmp/'
TESTDBNAME           = 'test2.db'

ANALYSIS_MODULES     = ['FastQC','DirectoryList','DirectorySize','Bowtie2']
DATABASE_DIR         = ['/n/home_rc/mclamp/Dropbox/databases/']
#DATABASE_DIR         = ['/n/regal/informatics/databases/']

logging.basicConfig(filename=LOGFILE,level=logging.INFO)

