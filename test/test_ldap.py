import ldap, sys

#ldap.set_option(ldap.OPT_REFERRALS, 0) 
#ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)          # use LDAP v3
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER) # allows a self-signed cert if using TLS 

AD_BIND_DN  = 'CN=clusterldap,OU=Unmanaged Service Accounts,DC=rc,DC=domain'
AD_BIND_PW  = 'p$e9e!A2'

class LdapConnection:

    def __init__(self):
        self.ldap_url  = "ldaps://dc2-rc.rc.fas.harvard.edu:636/"
        #self.ldap_url  = "ldaps://dc2-rc.rc.fas.harvard.edu:3268/"
        self.ldap_conn = ldap.initialize(self.ldap_url)

        print self.ldap_conn

        self.ldap_conn.simple_bind_s(AD_BIND_DN,AD_BIND_PW)


    def search(self, filter, search_fields_to_retrieve):

            results = self.ldap_conn.search_ext_s("OU=Domain Users,DC=rc,DC=domain", ldap.SCOPE_SUBTREE, filter, search_fields_to_retrieve)  
            return results

if __name__ =='__main__':

    filter = '(&(objectClass=person)(uid=%s))' % 'mclamp'

    ld = LdapConnection()
    results = ld.search(filter,['*'])

    for r in results:
        print r.__dict__
