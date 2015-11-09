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


# LDAP settings
import ldap, sys, md5
ldap.set_option(ldap.OPT_REFERRALS, 0) 
""" use LDAP v3 """
ldap.set_option (ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3) 

""" allows a self-signed cert is using TLS """
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)      

#ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_HARD   )
""" variables used in functions to specify an ldap server """
RC_DOMAIN = 'RC'
CGR_DOMAIN = 'CGR'
MCB_DOMAIN = 'MCB'
NUCLEUS_DOMAIN = 'NUCLEUS'
OEB_DOMAIN = 'OEB'
CCB_DOMAIN = 'CCB'
# Right now, we're ONLY using RC
ALL_WORKING_DOMAINS = [RC_DOMAIN]

""" RCG dn, to check if members are in RCG """
RCG_DN = 'CN=Research Computing,OU=Domain Groups,OU=CGR,DC=rc,DC=domain'
#RCG_DN = 'CN=Research Computing,OU=Domain Groups,DC=cgr,DC=harvard,DC=edu'
#DOT_HARVARD_EDU = '.harvard.edu'
#DOMAIN = '.domain'
AD_SEARCH_FIELDS = ['*']

""" ldap server user/pw """
#AD_BIND_DN = 'LDAP-RCG-WEBAPP-DEV@rc.domain'
#AD_BIND_PW = 'Sp1n4lD3v'
#AD_BIND_DN = 'LDAP-RCG-WEBAPP-PRD@nucleus.harvard.edu'
AD_BIND_DN = 'LDAP-RCG-WEBAPP-PRD@rc.domain'
AD_BIND_PW = 'AatTXx^$#'

#AD_BIND_DN = 'drupal'
# This is the password of the GuestBindAccount
#AD_BIND_PW = 'dr00p3rB!'


class LdapConnection:

    def __init__(self, ldap_server=None):
        self.ldap_url  = "something here"
        self.ldap_conn = ldap.initialize(self.ldap_url)
        self.ldap_conn.simple_bind_s(AD_BIND_DN, AD_BIND_PW)

    def search(self, filter, search_fields_to_retrieve):
        """ search based on a filter and fields to retrieve """
        try:
            results = self.ldap_conn.search_ext_s( self.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, filter, search_fields_to_retrieve)  
            return results
        except ldap.NO_SUCH_OBJECT:
            return None

    def add_member_and_unbind(self, instrument_cn, member_dn):
        """ add a member to an instrument group and then unbind """

        if member_dn == None:
            return False

        try:
            self.ldap_conn.modify_s(instrument_cn, [(ldap.MOD_ADD, "member", member_dn)]) 
        except:
            self.unbind()        
            return False
            
        self.unbind()        
        return True
        
    def remove_member_and_unbind(self, instrument_cn, member_to_remove_dn):
        """ remove a member from an instrument group and then unbind """
    
        if member_to_remove_dn == None:
            return False

        try:
            self.ldap_conn.modify_s(instrument_cn, [(ldap.MOD_DELETE, "member", member_to_remove_dn)]) 
        except:
            self.unbind()        
            return False
            
        self.unbind()        
        return True

    
"""
    Note: This is a potentially expensive method, was previously hard-coded,
    not going to db for LDAP connection info.  May be the way to go . . .
"""
def get_search_dn_url(s):
    """ Get a search dn and ldap url based on the string 's' """
    #msgt('get_search_dn_url: %s' % s)
    
    if s == None:
        return (None, None)
    
    """ check against the name: e.g. CGR, MCB, NUCLEUS, etc """
    ad_list = ActiveDirectoryDomainInfo.objects.filter(name=s)
    if len(ad_list) > 0:
        return ad_list[0].get_search_dn_and_url()

    """ check against the dc_snippet, e.g. 'DC=cgr', 'DC=mcb', etc """
    for ad in ActiveDirectoryDomainInfo.objects.all():
        if s.find(ad.dc_snippet) > -1:
            return ad.get_search_dn_and_url()
            
    """ check against the principal name, e.g. person@cgr.harvard.edu """
    try:
        parts = s.split('@')
        #This assumes that the first item after the @ symbol and before the first period
        #is the domain name, e.g. "rc", "cgr", etc.
        domain = parts[1].split('.')[0]
        #print domain
        #remainder = parts[1].partition('.')[2]
        #msg(parts)
        #p2 = parts[-1].replace(DOMAIN, '').upper()
        #p2 = p2.replace(DOT_HARVARD_EDU, '').upper()
        #p2 = parts[-1].replace(DOT_HARVARD_EDU, '').upper()
        #msg(p2)
        ad_list = ActiveDirectoryDomainInfo.objects.filter(name=domain)
        if len(ad_list) > 0:
            return ad_list[0].get_search_dn_and_url()
    except:
        pass
            
         
    return (None, None)

def test_server_connections():

    ldap_server_list = [RC_DOMAIN,]
    #ldap_server_list = [RC_DOMAIN, CGR_DOMAIN, MCB_DOMAIN, OEB_DOMAIN, CCB_DOMAIN, NUCLEUS_DOMAIN]
    cnt = 0
    for ldap_server in ldap_server_list:
        cnt +=1
        msgt('(%s/%s) Testing server: %s' % (cnt, len(ldap_server_list), ldap_server))
        try:
            if ldap_server == RC_DOMAIN:
                filter = '(&(objectClass=person)(userPrincipalName=%s))' % 'emattison@rc.domain'
            else:
                filter = '(&(objectClass=person)(userPrincipalName=%s))' % 'emattison@cgr.harvard.edu'
            ldap_conn = LdapConnection(ldap_server)
            msg(ldap_conn)
            result = ldap_conn.search_and_unbind(filter)
        except:
            result = None
            pass

        #msgt('>>> result: %s' % result)
        if result==None or result==[]:
            msg('no result')
        else:
            common_name, ad_lookup = result[0]
            if common_name == None:
                msg('No group found for filter "%s"' % filter)
            else:
                if not 'keys' in dir(ad_lookup): 
                    msg('nada')
                else:
                    print  MemberInfo(ad_lookup)

def test_ldap_upn():
    userPrincipalName = 'emattison@rc.domain'
    ldap_conn = LdapConnection(userPrincipalName)
    print ldap_conn

if __name__ =='__main__':
    from spinal_website.apps.auth_active_directory.helper_classes import *
    test_server_connections()
    #test_ldap_upn()


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
