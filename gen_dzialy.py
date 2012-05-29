# -*- coding: iso-8859-2 -*-

import ldap
import os
import sys
import re

import phoneldap.ldapfe as ldapfe
import phoneldap.util as util
import phoneldap.cmxml as cmxml
import phoneldap.util as util
import phoneldap.ldaputil as ldaputil

import plac

import pickle

from collections import defaultdict

DEFAULT_PATH = 'groups'
DEFAULT_FORMAT = 'html'
GROUP_DISPLAY_SEP = ':'

def save_page(path_templ, rendered_page, number):
    path = path_templ % {'number': number}
    open(path, 'w').write(rendered_page)

def save_pages(pages, path_templ, url_templ):
    rendered_pages = util.render_pages(pages, url_templ)
    for pos, rendered_page in enumerate(rendered_pages):
        util.save_page(path_templ, rendered_page, pos)

def get_id_label(group):
    group_parts = group.split(GROUP_DISPLAY_SEP)
    group_name = group_parts[0]
    group_display = group_parts[1] if len(group_parts) > 1 else group_name
    return group_name, group_display

def fetch_groups(l, config, groups_specs):
    groups_pages = {}
    for group_id, group_label in groups_specs:
        users = ldaputil.get_users(l, config, group_id)
        groups_pages[group_label] = users

def parse_groups_from_all(l, config, users):
    d = defaultdict(list)
    for user in users:
        ou = user['ou']
        d[ou].append(user)
    return d

@plac.annotations(
   # group_str=('Group', 'positional', None, str),
   dest_path=('Destination path', 'positional', None, str),
   format=('Output format', 'option', 'f', str),
   url_prefix=('URL prefix', 'option', 'u', str)
   )
def run(dest_path, format=DEFAULT_FORMAT, url_prefix=''):
    try:
        config = util.read_config()
        l = ldaputil.setup_ldap(config)

        # groups_specs_str = group_str.split(',')
        # groups_specs = [get_id_label(group) for group in groups_specs_str]
        # groups_pages = fetch_groups(l, config, groups_specs)

        all_ou_users = ldaputil.get_all_ou_users(l, config)
        groups_pages = parse_groups_from_all(l, config, all_ou_users)

        if format == 'pickle':
            pickle.dump(open(dest_path, 'wb'))
        if format == 'json':
            import json
            json.dump(groups_pages, open(dest_path, 'wb'), sort_keys=True, indent=4, encoding='utf-8')
        else:
            for group, pages in groups_pages.items():
                group_path = os.path.join(DEFAULT_PATH, group)
                if not os.path.exists(group_path):
                    os.makedirs(group_path)
                path_templ = '%s/page%%(number)d.html' % group_path
                url_templ = url_prefix + '/' + path_templ
                save_pages(pages, path_templ, url_templ)

    except ldap.LDAPError, e:
        print type(e)


def main():
    plac.call(run)


if __name__ == '__main__':
    main()

        
