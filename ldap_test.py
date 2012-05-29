import ldap
import os
import sys

import phoneldap.ldapfe as ldapfe
import phoneldap.util as util
import phoneldap.ldaputil as ldaputil


try:
    #dept = sys.argv[1]
    config = util.read_config()

    l = ldaputil.setup_ldap(config)
    #users = ldapfe.getAllOUMembers(l, config['people_dn'])
    users = ldaputil.get_all_ou_users(l, config)

    for user in users:
        print user

    print ldapfe.searchUser(l, config['people_dn'], 'cn=*Winters*')
except ldap.LDAPError, e:
    print type(e)
