import ldap, sys, md5

ldap.set_option(ldap.OPT_REFERRALS, 0) 
ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)          """ use LDAP v3 """
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)  """ allows a self-signed cert if using TLS """

RCG_DN           = 'CN=Research Computing,OU=Domain Groups,OU=CGR,DC=rc,DC=domain'

AD_BIND_DN = 'LDAP-RCG-WEBAPP-PRD@rc.domain'
AD_BIND_PW = 'AatTXx^$#'

class LdapConnection:

    def __init__(self, ldap_server=None):
        self.ldap_url  = ""
        self.ldap_conn = ldap.initialize(self.ldap_url)
        self.ldap_conn.simple_bind_s(AD_BIND_DN, AD_BIND_PW)


    def search(self, filter, search_fields_to_retrieve):
        """ search based on a filter and fields to retrieve """
        try:
            results = self.ldap_conn.search_ext_s( self.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, filter, search_fields_to_retrieve)  
            return results
        except ldap.NO_SUCH_OBJECT:
            return None

if __name__ =='__main__':

    filter = '(&(objectClass=person)(userPrincipalName=%s))' % 'emattison@rc.domain'
    from spinal_website.apps.auth_active_directory.helper_classes import *
    test_server_connections()
    #test_ldap_upn()
