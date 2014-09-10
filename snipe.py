import requests
import json


def login(session):
    request_file = open("request/login.req")
    login_request = json.loads(request_file.read())
    request_file.close()
    
    config_file = open("config/user.cfg")
    user_data = json.loads(config_file.read())
    config_file.close()

    login_request["post_data"]["userid"] = user_data["user"]
    login_request["post_data"]["pass"] = user_data["pass"]


    session.post(login_request["url"],login_request["post_data"])

login(0)
#session = requests.session()
