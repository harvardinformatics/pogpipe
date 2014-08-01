from argparse  import ArgumentParser
from config    import settings

import importlib
import logging
import os
import sys
import csv
import pprint

def main(args):

    # Maybe we should do this another way
    username = fetch_username_from_args(args)

    [user] = RCUser.filter(username=username)

    oldstr    = print_user_fields(user)

    if args.first_name:
        user.first_name = args.first_name

    if args.last_name:
        user.last_name  = args.last_name

    if args.email:
        user.email      = args.email

    # Now state
    if args.state == "active":
        user.is_active = True
    if args.state == "disabled":
        user.is_active = False

    if ! Portal_AD_Factory::check_user(user):
        exit()

    newstr = print_user_fields(user)

    print oldstr,newstr

    if args.store:
        user.save()
        Portal_AD_Factory::save_user(user)

def fetch_username_from_args(args):
    username    = args.username
    tmpusername = null;

    if args.email:
        tmpusername = Portal_AD_Factory::get_username_from_email(args.email)

        if tmpusername != null and username != null:
            if tmpusername != username:
                exit("username and email refer to different users.  please check input data")
    
    if username:
        return username

    if tmpusername:
        return tmpusername





if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Modify existing user in  portal and AD')

    parser.add_argument('-u','--username'   , help='AD Username')
    parser.add_argument('-e','--email'      , help="Email address")
    parser.add_argument('-f','--first_name' , help="First name")
    parser.add_argument('-l','--last_name'  , help="Last name")
    parser.add_argument('-c','--cluster'    , help="Add/remove cluster access [1/0]")
    parser.add_argument('-t','--state'      , help="Account state [active|disabled]")
    parser.add_argument('-d','--home_dir'   , help="Home directory (will generate one if --cluster 1")
    parser.add_argument('-s','--store'      , help="Saves the user to portal and AD")
    
    args = parser.parse_args()

    main(args)
