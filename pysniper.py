from __future__ import print_function

import requests
import warnings
import json
import re

from lxml import html

# warnings.filterwarnings("ignore")

def do_request(request_list, session=None, data=None, config=None):
    post_data = data or {}
    config = config or {}
    # create session if none given
    session = session or requests.Session()

    def replace_conf_var(string):
        def replace_variable(match):
            return config.get(re.sub(r'[^a-zA-Z0-9]', '', match.group()), '')
        return re.sub(r'{%.*?%}', replace_variable, string)

    # cycle through request list
    for req in request_list:
        # if no url given continue
        if not req.get('url'):
            continue

        print('{}: {}'.format(req.get('method','GET'),req.get('url')))

        res = None

        # update post_data with fields given in the request definition
        if req.get('post_data'):
            for key in req.get('post_data'):
                post_data[key] = replace_conf_var(req['post_data'][key])

        if req.get('debug'):
            print(post_data)

        # by default verify ssl certificates
        verify_ssl = req.get('verify',True)
        # if method post send 
        if req.get('method') == "POST":
            res = session.post(req.get('url'),data=post_data,verify=verify_ssl)
        else:
            res = session.post(req.get('url'),verify=verify_ssl)

        if req.get('output'):
            print(res.text)

        # TODO check for response state and decide for continue or break

        dom = html.fromstring(res.text)

        # handle response - parse form
        if req.get('parse_form'):
            input_fields = dom.xpath(req.get('parse_form'))

            # populate post data from xpath'ed input fields
            post_data={}
            for field in input_fields:
                if field.get('name'):
                    post_data[field.get('name')] = field.get('value', '')

        stop = False
        if req.get('tests'):
            for test in req.get('tests'):

                # find dom elements to check 
                elements = dom.xpath(test.get('xpath'))

                # if no dom elements found continue
                if not elements:
                    continue

                # if no match clause just proceed
                if not test.get('match'):
                    print(test.get('message',''))
                    if not test.get('continue'): stop = True
                    continue

                # replace config variable in match clause
                needle = replace_conf_var(test.get('match',''))

                # match needle against elements texts
                regex = re.compile(needle)
                for element in elements:
                    if regex.match(element.text):
                        print(test.get('message',''))
                        if not test.get('continue'): stop = True
        
        if stop:
            return session

def load_json(file_name):
    json_data = {}
    try:
        with open(file_name) as f:
            json_data = json.loads(f.read())
    except (OSError, IOError) as e:
        print("Could not open file {}, {}:".format(file_name, e))
    return json_data

login_request = load_json("request/login.json")
user_data = load_json("config/user.cfgg")

do_request(login_request,config=user_data)
