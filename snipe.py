import requests
import json

from lxml import html

#def checkResponse(response,checklist):

def login():
    session = requests.session()

    request_file = open("request/login.req")
    login_request = json.loads(request_file.read())
    request_file.close()
    
    config_file = open("config/user.cfg")
    user_data = json.loads(config_file.read())
    config_file.close()
    
    # get all the fancy ebay cookies
    session.get(login_request['prefetch_url'],verify=False)

    # get the login form and extract all fields
    login_page = session.get(login_request['login_url'],verify=False)
    dom = html.fromstring(login_page.text)

    input_fields = dom.xpath('//form[@name="SignInForm"]//input')
    
    # populate post data for login
    post_data={}
    for field in input_fields:
        post_data[field.name] = field.value
        # print(field.attrib['name'],': ',field.attrib['value'])

    # change values if any given in request file
    if login_request.get('post_data'):
        for key in login_request['post_data']:
            post_data[key] = login_request['post_data'][key]

    # add login and password from user.cfg
    post_data['userid'] = user_data['user']
    post_data['pass'] = user_data['pass']

    # do login
    response = session.post(login_request["login_url"],data=post_data,verify=False)
    print(response.text)
    # do after login redirect (done with javascript in browsers)
    my_ebay_page = session.get(login_request["after_login_url"])
    


    return session
    #return checkResponse(response,login_request["responses"])

session = login()
