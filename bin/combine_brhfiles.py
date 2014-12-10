from argparse  import ArgumentParser

import importlib
import logging
import os
import sys
import csv
import pprint
import re
 
from config import settings

def main(args):

    logging.info(" ========> combine_brhfiles.py")

    logging.info("ARGS %s"%args)

    print args
    try:

      stubs = [args.anchor]

      for file in os.listdir(args.directory):

         if file.endswith('.brh.dat'):
             
            match = re.match(args.anchor+'-(.*)\.brh\.dat',file)

            if match:
              stub  = match.group(1)
              print stub
              stubs.append(stub)


      print stubs

      i = 1
      hits = {}
      qids = []

      while i < len(stubs):

        stub0 = stubs[0]
        stub1 = stubs[i]

        print stub0
        print stub1

        brhfile = stub0 + "-" + stub1 + ".brh.dat"
        brhfile = os.path.join(args.directory,brhfile)

        if not os.path.isfile(brhfile):
          raise IOError("BRH file [%s] not found"%brhfile)


        with open(brhfile) as fp:

           for line in fp:

              line = line.rstrip('\n') 
              f    = line.split('\t',5)

              found = int(f[1])

              if found == 1:
                  qid = f[2]
                  hid = f[3]

                  if qid not in hits:
                     hits[qid] = {}

                  if stub1 not in hits[qid]:
                     hits[qid][stub1] = {}

                  hits[qid][stub1]['hid'] = hid
                  hits[qid][stub1]['line'] = line 

        i = i + 1

      qids = hits.keys()

      for qid in qids:
         tmpstr = qid

         i     = 1
         count = 0

         while i < len(stubs):
           hid = '-'

           if stubs[i] in hits[qid]:
             hid = hits[qid][stubs[i]]['hid']
             count = count + 1

           tmpstr += "\t" + hid
           i = i + 1 

         print tmpstr + "\t" + str(count) + "\n"
     
    except IOError as e:
      print e

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Combine all best reciprocal hit files into one file')

    parser.add_argument('-a','--anchor'   , help='Species to anchor on')
    parser.add_argument('-d','--directory', help='Directory to look in')
    
    args = parser.parse_args()

    main(args)

