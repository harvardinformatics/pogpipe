from   config                   import settings
from   ftplib                   import FTP

import os
import re
import logging

""" Inherit from Analysis? """

class UCSCDownloader():

    """Class to download genome fasta and gene annotation from UCSC """

    genome_name    = None
    dest_topdir    = None
    dest_genomedir = None

    def __init__(self,genome_name):
        
        #super(UCSCDownloader,self).__init__(self.name)
        
        self.genome_name  = genome_name

        self.ftp_sitename = "hgdownload.cse.ucsc.edu"
        self.ftp_topdir   = "/goldenPath"
        self.ftp_fastadir = "bigZips"



    def getFastaDir(self):

        return  self.ftp_topdir + "/" + self.genome_name + "/" + self.ftp_fastadir


    def fetchFile(self,src_dir,src_file,dest_dir,check_md5=False,overwrite=False):


        """ Gets a file from the UCSC website and optionall checks the md5sum (expects filename.md5 to be there)."""

        dest_file = dest_dir + "/" + src_file

        if overwrite == False and os.path.exists(dest_file):
            
            raise Exception("Destination file  %s exists.  Use overwrite option to overwrite"%dest_file)


        if os.path.exists(dest_dir) == False:

            os.makedirs(dest_dir)


        self.connect()

        self.changeDir(src_dir)


        with open(dest_dir + "/" + src_file, 'w+b') as f:
            print "Fetching %s to %s"%(src_file,dest_dir)
            
            res = self.ftp.retrbinary('RETR %s' % src_file, f.write)




    def fetchGenomeSoftmaskedFasta(self,dest_topdir,overwrite=False):

        """ Goes to the UCSC ftp site and downloads softmasked chromosomal fasta """

        ftp_dir        = self.getFastaDir()

        dest_genomedir = dest_topdir + "/" + self.genome_name

        fasta_file     = self.findSoftmaskedFastaFile(ftp_dir)

        checkfile = self.checkExistingFile(dest_genomedir,ftp_dir,fasta_file)

        if checkfile == False or overwrite == True:

            self.fetchFile(ftp_dir,
                           fasta_file,
                           dest_genomedir,
                           False,
                           overwrite)

            
        # Check md5?

        # Now we need to unzip

        # Create a single fasta

        # Index the single fasta for fetching pieces using samtools


    def fetchGenomeRefMrnaFasta(self,dest_topdir,overwrite=False):

        """ Gets fasta file for mrna from UCSC ftp site """


        ftp_dir        = self.getFastaDir()

        dest_genomedir = dest_topdir + "/" + self.genome_name

        fasta_file     = self.findRefMrnaFastaFile(ftp_dir)

        checkfile = self.checkExistingFile(dest_genomedir,ftp_dir,fasta_file)

        if checkfile == False or overwrite == True:

            self.fetchFile(ftp_dir,
                           fasta_file,
                           dest_genomedir,
                           False,
                           overwrite)


    def fetchRefGeneCoords(self,dest_topdir,overwrite=False):

        """ Gets coordinates (in ? format) for reference genesetfrom UCSC ftp site"""


    def findSoftmaskedFastaFile(self,src_dir):

        self.connect()
        
        self.changeDir(src_dir)

        files = self.ftp.nlst()

        print "Files are %s"%files

        filelist = ['chromFa.tar.gz',self.genome_name + ".fa.gz"]

        for f in files:

            for ff in filelist:
                if f == ff:
                    return ff

        raise Exception("No recognizable softmasked fasta file.  Looked for %s.   Files in dir are %s"%(filelist,files))


    def findRefMrnaFastaFile(self,src_dir):

        self.connect()
        
        self.changeDir(src_dir)

        files = self.ftp.nlst()

        print "Files are %s"%files

        filelist = ['refMrna.fa.gz']

        for f in files:

            for ff in filelist:
                if f == ff:
                    return ff

        raise Exception("No recognizable softmasked fasta file.  Looked for %s.   Files in dir are %s"%(filelist,files))

    def checkExistingFile(self,dest_dir,src_dir,src_file):

        self.ftp.sendcmd("TYPE i")    # Change to binary mode

        src_size  = self.ftp.size(src_dir + "/" + src_file)
        dest_size = None

        if os.path.exists(dest_dir + "/" + src_file):
            dest_size = os.path.getsize(dest_dir + "/" + src_file)
        else:
            return False

        if dest_size == src_size:
            print "File sizes agree for file %s srcdir %s destdir %s"%(src_file,src_dir,dest_dir)
            return True
        else:
            return False
            
        


    def connect(self):

        """ Initial connection to the UCSC ftp site"""

        ftp = FTP(self.ftp_sitename)   # connect to host, default port

        ftp.set_debuglevel(2)
        ftp.set_pasv(True)

        ftp.login()                    # user anonymous, passwd anonymous@

        self.ftp = ftp


    def changeDir(self,src_dir):
        print "Changing to directory %s"%src_dir

        self.ftp.cwd(src_dir)


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',level=logging.DEBUG)

    obj = UCSCDownloader('hg19')

    obj.fetchGenomeSoftmaskedFasta('/Users/mclamp/genomes/')
    obj.fetchGenomeRefMrnaFasta('/Users/mclamp/genomes/')

