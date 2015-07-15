from argparse  import ArgumentParser

import importlib
import logging
import os
import sys
import csv
import pprint
 
from config import settings

def main(args):

    logging.info(" ========> parse_besthits.py")

    logging.info("ARGS %s"%args)

    try:


      hits1 = {}
      hits2 = {}

      prev = None

      with open(args.file1) as fp1:

         for line in fp1:
             
             line = line.rstrip('\n')

             ff   = line.split('\t')

             qid = ff[0]
             hid = ff[1]

             if not prev or prev != qid:

               if qid not in hits1:
                  hits1[qid] = {}

               hits1[qid]['hid']  = hid
               hits1[qid]['line'] = line 

             prev = qid

      print hits1.keys()

    except IOError as e:
      print e

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Parse blast best hits script')

    parser.add_argument('--file1'   , help='First file to parse')
    parser.add_argument('--file2'   , help='Second file to parse')
    
    args = parser.parse_args()

    main(args)

