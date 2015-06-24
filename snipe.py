import requests
import json

from lxml import html

def checkResponse(response,checklist):

def login(session):
    request_file = open("request/login.req")
    login_request = json.loads(request_file.read())
    request_file.close()
    
    config_file = open("config/user.cfg")
    user_data = json.loads(config_file.read())
    config_file.close()

    login_request["post_data"]["userid"] = user_data["user"]
    login_request["post_data"]["pass"] = user_data["pass"]

    referer = session.get(login_request['prefetch'])
    page = session.get(login_request['url'])
    dom = html.fromstring(page.text)

    input_fields = dom.xpath('//form[@name="SignInForm"]//input')
    
    for field in input_fields:
        print(field.attrib['name'],': ',field.attrib['value'])
    #session.post(login_request["url"],login_request["post_data"])
    #return checkResponse(response,login_request["responses"])

session = requests.session()
login(session)
