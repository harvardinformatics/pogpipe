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
        self.ldap_conn = ldap.initialize(self.ldap_url)
        self.base_dn   = "OU=Domain Users,DC=rc,DC=domain"

        print self.ldap_conn

        self.ldap_conn.simple_bind_s(AD_BIND_DN,AD_BIND_PW)


    def search(self, filter, search_fields_to_retrieve):

            results = self.ldap_conn.search_ext_s(self.base_dn, ldap.SCOPE_SUBTREE, filter, search_fields_to_retrieve)  
            return results

    def username_exists(self,username):
        try:
            user_results = self.ldap_conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE,
                                       '(&(sAMAccountName=' +
                                       username +
                                       ')(objectClass=person))',
                                       ['distinguishedName'])
        except ldap.LDAPError, error_message:
            print "Error finding username: %s" % error_message
            return False
        
        if len(user_results) != 0:
           return user_results[0][1]['distinguishedName'][0]
        else:
            return False

    def email_exists(self,email):
        try:
            user_results = self.ldap_conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE,
                                                   '(&(mail=' +
                                                   email +
                                                   ')(objectClass=person))',
                                                   ['distinguishedName'])
        except ldap.LDAPError, error_message:
            print "Error finding email: %s" % error_message
            return False
        
        if len(user_results) != 0:
            return user_results[0][1]['distinguishedName'][0]
        else:
            return False



    def delete_user(self,displayname):
        try:
            ld.ldap_conn.simple_bind_s("account@rc.domain",'Formula350!')
            
        except ldap.LDAPError, error_message:
            print "Error connecting to LDAP server: %s" % error_message
            return False
        
        dn="cn="+displayname+",OU=Domain Users,DC=rc,DC=domain"
        
        print dn + "\n"

        try:
            
            self.ldap_conn.delete_s(dn)
            
        except ldap.LDAPError, error_message:
            print "Error deleting username [%s] (%s)"%(username,error_message)
            return False
        

    def get_max_uidnumber(self):

        users = self.get_all_user_entries(['uidNumber']);
        uids  = []

        #uids = sorted(users, key=lambda u: u['uidNumber'])
        for u in users:
            if users[u]['uidNumber'] is not None:
                uids.append( int(users[u]['uidNumber']))

                maxuid = max(uids);
        
        return maxuid

    def get_all_user_entries(self,attr):

        try:
            ld.ldap_conn.simple_bind_s("account@rc.domain",'Formula350!')
            
        except ldap.LDAPError, error_message:
            print "Error connecting to LDAP server: %s" % error_message
            return False

        filter =  '(&(cn=*)(objectClass=person))'

        if 'cn' not in attr:
            attr.append('cn')
        
        results = self.ldap_conn.search_ext_s(self.base_dn, ldap.SCOPE_SUBTREE, filter, attr)  

        users   = {}

        if len(results) != 0:
            for res in results:

                tmpuser = {}
                
                for arg in attr:
                    tmpuser[arg] = []

                    if arg in res[1]:
                        i = 0;

                        while i < len(res[1][arg]):
                            argval = res[1][arg][i]
                            tmpuser[arg].append(argval)                        
                            i = i+1
                        
                        if len(tmpuser[arg]) == 1:
                            tmpuser[arg] = tmpuser[arg][0]
                    else:
                        tmpuser[arg] = None
                      
                users[tmpuser['cn']] = tmpuser

        return users

if __name__ =='__main__':

    filter = '(&(objectClass=person)(uid=%s))' % 'mclamp'

    ld = LdapConnection()

    username = "pogtest"
    password = "98Pogg76"
    firstname = "Pog"
    surname  = "Test"
    email    = "pog@pogtest.com"

    displayname = '%s %s' % (firstname, surname)

    dn="cn="+displayname+",OU=Domain Users,DC=rc,DC=domain" # % (username, AD_SEARCH_DN)


    
    ld.delete_user(displayname)

    if ld.email_exists(email):
        print "User Email [%s] exists.  Can't create.\n"%email;
        exit()

    if ld.username_exists(username):
        print "User [%s] exists.  Can't create.\n"%username;
        exit()
        

    uidnum = ld.get_max_uidnumber()

    # A dict to help build the "body" of the object
    attrs = {}
    attrs['objectclass']        = ['top','person','organizationalPerson','user']
    attrs['cn']                 = displayname
    attrs['sAMAccountname']     = str(username)
    attrs['userPassword']       = str(password)
    attrs['givenName']          = str(firstname)
    attrs['sn']                 = str(surname)
    attrs['displayName']        = str(displayname)
    attrs['uid']                = str(username)
    attrs['mail']               = email
    attrs['userAccountControl'] = '514'                             # disabled
    attrs['userPrincipalName']  = username

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

    try:
        ld.ldap_conn.simple_bind_s("account@rc.domain",'xxxxxxxxxx')
    except ldap.LDAPError, error_message:
        print "Error connecting to LDAP server: %s" % error_message
        exit()

    try:
        ld.ldap_conn.add_s(dn,ldif)
    except ldap.LDAPError, error_message:
        print "Error adding new user: %s" % error_message
        exit()

