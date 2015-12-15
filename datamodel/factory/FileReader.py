import os
import sys
import os.path
import logging
import importlib

class FileReader(object):
   
    fh   = None
    lnum = 0

    def __init__(self,file):
        self.filename = file
        self.fh       = open(file)
        self.lnum     = 0

    def nextLine(self):
       
        while True:
            str =  self.fh.readline()

            if not str: break

            self.lnum = self.lnum + 1
            return str
    
           
