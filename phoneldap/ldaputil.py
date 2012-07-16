import ldap
import ldapfe
import operator

def setup_ldap(config):
    l = ldap.open(config['hostname'], port=config['port'])
    l.simple_bind_s(config.get('username', ''), config.get('password', ''))
    return l

def get_ou_users(l, config, ou):
    users = ldapfe.getOUMembers(l, config['people_dn'], ou)
    return ldapfe.parse_users(users)

def get_all_ou_users(l, config):
    users = ldapfe.getAllOUMembers(l, config['people_dn'])
    return ldapfe.parse_users(users)
