# -*- coding: iso-8859-2 -*-

import os
import re

import pycisco.cmpush as cmpush
import pycisco.cmxml as cmxml

def read_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(os.path.expanduser('~'), '.ldaprc')
    config = eval(open(config_path).read())
    config['groups_dn'] = 'ou=Groups,' + config['base_dn']
    config['people_dn'] = 'ou=People,' + config['base_dn']
    return config

intab = u"ąćęłńóśżźĄĆĘŁŃÓŚŻŹ"
ottab = u"acelnoszzACELNOSZZ"

def translate(s):
    for i, o in zip(intab, ottab):
        s = re.sub(i, o, s)
    return s

LIMIT = 32


def paginate_users(users, limit=LIMIT):
    pages = []
    for pos, user in enumerate(users):
        if pos % limit == 0:
            currPage = []
            pages.append(currPage)
        currPage.append(user)
    return pages

def format_menu(title, prompt, items):
    data = cmxml.MENU_HEADER % {'title': title, 'prompt': prompt}
    for name, url in items:
        data += cmxml.MENU_ITEM % {'name': name, 'url': url}
    data += cmxml.MENU_FOOTER
    return data

def format_page(title, prompt, page, next_url=None, prev_url=None):
    data = cmxml.DIRECTORY_HEADER % {'title': title, 'prompt': prompt}
    for entry in page:
        name = u'%s %s' % (entry['lastName'], entry['firstName'])
        name = translate(name)

        telephone = entry['telephoneNumber']
        data += cmxml.DIRECTORY_ENTRY % {'name': name, 'telephone': telephone}


    data += cmxml.SOFTKEY_ITEM % {'name': 'Dial', 'url': 'SoftKey:Dial', 'position': 1}
    data += cmxml.SOFTKEY_ITEM % {'name': 'EditDial', 'url': 'SoftKey:EditDial', 'position': 2}


    data += cmxml.SOFTKEY_ITEM % {'name': 'Cancel', 'url': 'SoftKey:Exit', 'position': 3}

    if prev_url is not None:
        data += cmxml.SOFTKEY_ITEM % {'name': 'Prev', 'url': prev_url, 'position': 4}

    if next_url is not None:
        data += cmxml.SOFTKEY_ITEM % {'name': 'Next', 'url': next_url, 'position': 5}

    data += cmxml.DIRECTORY_FOOTER
    return data

def render_page(page, next_url=None):
    return format_page('Dzialy', 'Dzialy', page, next_url)

def render_pages(pages, url_templ):
    next_urls = [url_templ % {'number': next_url} for next_url in range(1, len(pages))] + [None]
    rendered_pages = [render_page(page, next_url) for page, next_url in zip(pages, next_urls)]
    return rendered_pages

