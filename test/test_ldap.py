import ldap, sys
import ldap.modlist as modlist

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

    username = "pogtest"
    password = "98Pogg76"
    firstname = "Pog"
    surname  = "Test"

    dn="cn=Pog Test,OU=Domain Users,DC=rc,DC=domain" # % (username, AD_SEARCH_DN)

    displayName = "Pog Test" #'%s %s [%s]' % (surname, firstname, username)

    # A dict to help build the "body" of the object
    attrs = {}
    attrs['objectclass'] = ['top','person','organizationalPerson','user']
    attrs['cn'] = str(username)
    attrs['sAMAccountname'] = str(username)
    attrs['userPassword'] = str(password)
    attrs['givenName'] = str(firstname)
    attrs['sn'] = str(surname)
    attrs['displayName'] = str(displayName)
    attrs['userPrincipalName'] = "%s at mail.domain.it" % username

    # Some flags for userAccountControl property
    SCRIPT = 1
    ACCOUNTDISABLE = 2
    HOMEDIR_REQUIRED = 8
    PASSWD_NOTREQD = 32
    NORMAL_ACCOUNT = 512
    DONT_EXPIRE_PASSWORD = 65536
    TRUSTED_FOR_DELEGATION = 524288
    PASSWORD_EXPIRED = 8388608

    # this works!
    attrs['userAccountControl'] = str(NORMAL_ACCOUNT + ACCOUNTDISABLE)

    # this does not work :-(
    #attrs['userAccountControl'] = str(NORMAL_ACCOUNT)
    
# Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)

    print ldif
    ld.ldap_conn.simple_bind_s("account@rc.domain",'Formula350!')
    ld.ldap_conn.add_s(dn,ldif)

