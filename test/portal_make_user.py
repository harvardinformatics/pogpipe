from argparse  import ArgumentParser
from config    import settings

import importlib
import logging
import os
import sys
import csv
import pprint

def main(args):

    newuser = new RCUser()

    # Check we have the essentials
    
    if ! args.first_name:
        exit()
    if ! args.last_name:
        exit()
    if ! args.email:
        exit()

    newuser.first_name = args.first_name
    newuser.last_name  = args.last_name
    newuser.email      = args.email
    newuser.is_active  = False
    newuser.username   = args.username

    # Generate a username if needed

    if newuser.username == "GENERATE":
        newuser.username = Portal_AD_Factory::generate_username(newuser)

    # Check the user doesn't exist by username or email

    if Portal_AD_Factory::username_exists(newuser.username):
        exit()

    if Portal_AD_Factory::email_exists(newuser.email):
        exit()

    # Now basic groups
    groups = ['Domain_Users','new_users']  # Do we need domain users?

    # Add cluster things
    if args.cluster == True:
        groups.push("cluster_users")
        homedir = Portal_AD_Factory::generate_home_dir(newuser)  # Is this an attribute?

    # Now state
    if args.state == "active":
        newuser.is_active = True
    if args.state == "disabled":
        newuser.is_active = False

    if ! Portal_AD_Factory::check_user(newuser):
        exit()

    print_user(newuser)

    if args.store:
        newuser.save()
        Portal_AD_Factory::save_user(newuser)



if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Add new user to portal and AD')

    parser.add_argument('-u','--username'   , help='AD Username. Value of GENERATE will make a unique one')
    parser.add_argument('-e','--email'      , help="Email address")
    parser.add_argument('-f','--first_name' , help="First name")
    parser.add_argument('-l','--last_name'  , help="Last name")
    parser.add_argument('-c','--cluster'    , help="Add cluster access",action="store_true")
    parser.add_argument('-n','--new'        , help="This is a new user")
    parser.add_argument('-t','--state'      , help="Account state [active|disabled]")
    parser.add_argument('-d','--home_dir'   , help="Home directory (will generate one if --cluster")
    parser.add_argument('-s','--store'      , help="Saves the user to portal and AD")
    
    args = parser.parse_args()

    main(args)
