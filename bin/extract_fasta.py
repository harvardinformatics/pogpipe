import re
import os
import sys
import unittest

from datamodel.factory.FastaFile  import FastaFile

import importlib


ff = FastaFile(sys.argv[1])
id = sys.argv[2]

seq = ff.nextSeq()

while seq is not None:
    if seq['id'] == id:
        str = FastaFile.toString([seq])
        print str
        exit()
    seq = ff.nextSeq()


