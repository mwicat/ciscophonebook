import ldap
import re
import model
import ldaphelper
import util


searchScope = ldap.SCOPE_SUBTREE

ATTR_CNAME = 'cn'
ATTR_GECOS = 'gecos'
ATTR_DN = 'dn'
ATTR_MEMBER = 'uniquemember'
ATTR_OU = 'ou'

ATTR_NUMBER = 'telephonenumber'
ATTR_TELEPHONE_NUMBER = 'telephonenumber'

INTERNAL_NUMBER_LEN = 4

ATTR_MOBILE_NUMBER = 'mobile'
ATTR_FIRST_NAME = 'givenname'
ATTR_LAST_NAME = 'sn'
ATTR_UID = 'uid'

def search(l, dn, filter=None):
    try:    
        result_set = l.search_s(dn, searchScope, filter) if filter is not None else l.search_s(dn, searchScope)
        result_set = ldaphelper.get_search_results(result_set)
    except ldap.NO_SUCH_OBJECT:
        result_set = []
    return result_set

def get_attr_value(record, attr):
    return record.get_attr_values(attr)[0] if record.has_attribute(attr) else None

def searchFirst(l, dn, filter=None):
    results = search(l, dn, filter)
    return results[0] if results else None

def formatNumber(num):
    return re.sub('\s+', '', num)

def formatExternalNumber(num):
    num = re.sub('\s+', '', num)
    num = '00' + num[1:]
    return num

def parseTelephoneAttr(telAttr):
    nums = [formatNumber(num) for num in telAttr.split('ext.')]
    external = formatExternalNumber(nums[0]) if nums[0] else None
    internal = nums[1] if len(nums) > 1 else None
    return external, internal

def getOUMembers(l, people_dn, ou):
    ou_filter = '%s=%s' % (ATTR_OU, ou)
    result_set = search(l, people_dn, ou_filter)
    return result_set

def getAllOUMembers(l, people_dn):
    ou_filter = '%s=*' % ATTR_OU
    result_set = search(l, people_dn, ou_filter)
    return result_set

def parse_users(results_data):
    users = [getUserInfo(data) for data in results_data]
    users = [user for user in users if user['telephoneNumber'] is not None]
    users.sort(key=lambda e: (e['lastName'], e['firstName']))
    return users

def searchUser(l, people_dn, filter):
    results_data = search(l, people_dn, filter)
    return parse_users(results_data)

def is_valid_internal_number(num):
    return num is not None and len(num) == INTERNAL_NUMBER_LEN

def getUserInfo(user):
    if user.has_attribute(ATTR_NUMBER):
        external, internal = parseTelephoneAttr(get_attr_value(user, ATTR_NUMBER))
    else:
        external = internal = None

    mobileNumber = get_attr_value(user, ATTR_MOBILE_NUMBER)
    mobileNumber = formatExternalNumber(mobileNumber[0]) if mobileNumber is not None else None

    telephoneNumber = get_attr_value(user, ATTR_TELEPHONE_NUMBER)
    telephoneNumber = telephoneNumber if is_valid_internal_number(telephoneNumber) else None

    user_info = dict(
        uid=get_attr_value(user, ATTR_UID),
        firstName=get_attr_value(user, ATTR_FIRST_NAME),
        lastName=get_attr_value(user, ATTR_LAST_NAME),
        ou=get_attr_value(user, ATTR_OU),
        mobileNumber=mobileNumber,
        telephoneNumber=telephoneNumber,
        externalNumber=external,
        internalNumber=internal)
    for key, value in user_info.items():
        if value is not None:
            value = value.decode('utf-8')
            value = util.translate(value)
            user_info[key] = value
    return user_info
