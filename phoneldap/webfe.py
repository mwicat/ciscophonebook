import ldap
import model
import util
import ldaputil
import ldapfe
import pickle

from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template

app = Flask(__name__)

SEARCH_ITEM_TITLE = 'Search'
GROUPS_ITEM_TITLE = 'Groups'

TEST_RESULTS = [model.UserInfo('mkowalski', 'marek', 'kowalski', '4353453', '435', '43534535') for i in range(100)]

def fetch_entries(l, phrase):
    phrase = '*%s*' % phrase
    filter = '(|(%s=%s)(%s=%s))' % (ldapfe.ATTR_CNAME, phrase, ldapfe.ATTR_GECOS, phrase)
    print 'filter', filter
    return ldapfe.searchUser(l, app.rc_config['people_dn'], filter)
    # return TEST_RESULTS


def make_xml_response(*args, **kw):
    response = make_response(*args, **kw)
    response.headers['content-type'] = 'text/xml'
    return response


def ext_url_for_self():
    return url_for(request.endpoint, _external=True, **request.view_args)


def ext_url_for(endpoint, **kw):
    return url_for(endpoint, _external=True, **kw)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    return 'AUTHORIZED'

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    title = 'Menu' 
    prompt = 'Choose'
    groups = app.groups_pages.keys()

    search_url = '%s' % ext_url_for('.users')
    sample_search_url = '%s?phrase=%s' % (search_url, 'a')
    groups_url = ext_url_for('.groups_list')

    items = [(SEARCH_ITEM_TITLE, search_url),
             (GROUPS_ITEM_TITLE, groups_url)]
    content = util.format_menu(title, prompt, items)
    return make_xml_response(content)    


@app.route('/groups', methods=['GET', 'POST'])
def groups_list():
    title = 'Groups' 
    prompt = 'Choose'
    groups = app.groups_pages.keys()
    items = [(group, ext_url_for('.groups', group=group)) for group in groups]
    items.sort(key=lambda (group, ext_url): group)
    content = util.format_menu(title, prompt, items)
    return make_xml_response(content)    


@app.route('/groups/<group>', methods=['GET', 'POST'])
def groups(group):
    page = int(request.args.get('page', 0))
    title = 'Group %s' % group
    prompt = 'Choose'
    pages = app.groups_pages[group]

    curr_url = ext_url_for_self()

    results_paged = pages[page] if 0 <= page < len(pages) else []
    prev_page = page - 1
    next_page = page + 1

    prev_url = '%s?page=%d' % (curr_url, prev_page) if prev_page >= 0 else None
    next_url = '%s?page=%d' % (curr_url, next_page) if next_page < len(pages) else None

    content = util.format_page(title, prompt, results_paged, prev_url=prev_url, next_url=next_url)
    return make_xml_response(content)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if not request.args:
        search_url = ext_url_for_self()
        return make_xml_response(render_template('search.xml', search_url=search_url))

    phrase = request.args.get('phrase')
    page = int(request.args.get('page', 0))

    l = ldaputil.setup_ldap(app.rc_config)
    results = fetch_entries(l, phrase)
    pages = util.paginate_users(results)

    title = 'Results for %s' % phrase
    prompt = 'Choose'

    curr_url = ext_url_for_self()

    results_paged = pages[page] if 0 <= page < len(pages) else []
    prev_page = page - 1
    next_page = page + 1

    prev_url = '%s?phrase=%s&amp;page=%d' % (curr_url, phrase, prev_page) if prev_page >= 0 else None
    next_url = '%s?phrase=%s&amp;page=%d' % (curr_url, phrase, next_page) if next_page < len(pages) else None

    content = util.format_page(title, prompt, results_paged, prev_url=prev_url, next_url=next_url)

    return make_xml_response(content)


