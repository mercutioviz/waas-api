import requests
import pprint
import sys
from getpass import getpass
from urllib.parse import urlencode, urljoin
import difflib

API_BASE = "https://api.waas.barracudanetworks.com/v2/waasapi/"


def waas_api_login(email, password):
    res = requests.post(urljoin(API_BASE, 'api_login/'), data=dict(email=email, password=password))
    res.raise_for_status()
    response_json = res.json()
    return response_json['key']


def waas_api_get(token, path):
    res = requests.get(urljoin(API_BASE, path), headers={'auth-api': token})
    res.raise_for_status()
    return res.json()

def is_app_present(apps_list, app_name):
    for app in apps_list:
        if app['name'] == app_name:
            app_present = app['id']
            break
        else:
            app_present = False

    return app_present


if __name__ == '__main__':
    if len(sys.argv) >= 5:
        email = sys.argv[1]
        password = sys.argv[2]
        app1name = sys.argv[3]
        app2name = sys.argv[4]
    else:
        email = input("Enter user email:")
        password = getpass("Enter user password:")
        app1name = input("Enter name of first WaaS app to compare:")
        app2name = input("Enter name of second WaaS app to compare:")
    token = waas_api_login(email, password)

    print("App1: " + app1name)
    print("App2: " + app2name)
    # Show list of applications, and servers for each application
    apps = waas_api_get(token, 'applications')

    # Verify that each of these apps is present
    app1 = is_app_present(apps['results'], app1name)
    if app1:
        print("App1 (" + app1name + ") found")
    else:
        sys.exit("App1 (" + app1name + ") not found")

    app2 = is_app_present(apps['results'], app2name)
    if app2:
        print("App2 (" + app2name + ") found")
    else:
        sys.exit("App2 (" + app2name + ") not found")

    print("App ids found: {} and {}".format(app1, app2))
    #pprint.pprint(app1)
    #pprint.pprint(app2)
    app1data = waas_api_get(token, "applications/" + str(app1) + "/")
    app2data = waas_api_get(token, "applications/" + str(app2) + "/")

    print("App1 data:")
    print(app1data)
    print("\nApp2 data:")
    print(app2data)
