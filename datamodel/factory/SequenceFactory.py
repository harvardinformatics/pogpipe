import os
import sys
import os.path
import logging
import importlib

from   config          import settings

class SequenceFactory(object):
    """Factory class that returns sequences or partial sequences given an id"""

    @staticmethod
    def getSequenceFromBlastDB(id,blastdb):

        bindir      = settings.TOOLDIR  + "/ncbi-blast-2.2.30+/bin/"
        progname    = "blastdbcmd"
        blastdbcmd  = bindir + progname

        cmd = self.blastdbcmd + " -db " + blastdb + " -entry " + id

        print "Command %s"%cmd

        p = Popen([cmd], 
                  shell     = True, 
                  stdout    = PIPE,
                  stderr    = PIPE,
                  close_fds = True)

        # Loop over the output - Johnny B likely has something to say about this

        output_str = ""

        while p.poll() == None:
            
            (out,err) = p.communicate()
            
                #print "OUT - %s"%out
                #print "ERR - %s"%err
            
            if out != '':
                output_str.append(out)
                sys.stdout.flush()

            if err != '':
                output_str.append(err)
                sys.stderr.flush()





