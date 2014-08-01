from argparse  import ArgumentParser
from config    import settings

import importlib
import logging
import os
import sys
import csv
import pprint

def main(args):

    username = args.username

    [user] = RCUser.filter(username=username)

    # How do I fetch groups?

    # Check group exists?

    

    if args.store:
        user.save()
        Portal_AD_Factory::save_user(user)

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Add a user to a group or groups')

    parser.add_argument('-u','--username'   , help='AD Username')
    parser.add_argument('-g','--group'      , help="groups (group1,group2)")
    parser.add_argument('-s','--store'      , help="Saves the user to portal and AD")
    
    args = parser.parse_args()

    main(args)
