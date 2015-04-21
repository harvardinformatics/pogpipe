import os
import sys
import os.path
import logging
import importlib

from   config          import settings
from   subprocess      import Popen, PIPE

class SequenceFactory(object):
    """Factory class that returns sequences or partial sequences given an id"""

    @staticmethod
    def getSequenceFromBlastDB(id,blastdb):

        bindir      = settings.TOOLDIR  + "/ncbi-blast-2.2.30+/bin/"
        progname    = "blastdbcmd"
        blastdbcmd  = bindir + progname

        cmd = blastdbcmd + " -db " + blastdb + " -entry " + id

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
            
            print "OUT - %s"%out
            print "ERR - %s"%err
            
            if out != '':
                output_str = output_str + out

                sys.stdout.flush()

                lines = output_str.split('\n')
                seqstr = ""
                seqid  = None

                for line in lines:
                    line = line.rstrip('\n')
                    ff   = line.split(' ')

                    if ff[0].startswith(">"):
                        seqid = ff[0].replace(">",'')
                    else:
                        seqstr = seqstr + line

                if seqid is not None:
                    seq = {}

                    seq['id']  = seqid
                    seq['seq'] = seqstr

                    return seq



            if err != '':
                output_str = output_str + err
                sys.stderr.flush()





