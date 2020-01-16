import requests
import sys
from getpass import getpass
from urllib.parse import urlencode, urljoin
import json
import argparse

API_BASE = "https://api.waas.barracudanetworks.com/v2/waasapi/"


def get_arguments():
    parser = argparse.ArgumentParser(description='Dumps the JSON config of a single WaaS application')
    parser.add_argument('-p',
                        '--pretty',
                        dest='pretty_print',
                        help='Display prettily formatted JSON output',
                        action='store_true',
                        default=False)
    parser.add_argument('-u',
                        '--email',
                        dest='email',
                        help='Email address for login',
                        metavar='email')
    parser.add_argument('-P',
                        '--password',
                        dest='password',
                        help='Password for login',
                        metavar='password'
                        )
    parser.add_argument('-a',
                        '--appname',
                        dest='appname',
                        help='Name of the application whose config will be displayed',
                        metavar='appname'
                        )

    arguments = parser.parse_args()

    return arguments


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
    args = get_arguments()
    if args.email:
        email = args.email
    else:
        email = input("Enter user email:")

    if args.password:
        password = args.password
    else:
        password = getpass("Enter user password:")

    if args.appname:
        app1name = args.appname
    else:
        app1name = input("Enter the name of the WaaS app whose configuration will be displayed:")

    pretty_print = args.pretty_print
    token = waas_api_login(email, password)
    # if len(sys.argv) >= 4:
    #     email = sys.argv[1]
    #     password = sys.argv[2]
    #     app1name = sys.argv[3]
    # else:
    #     email = input("Enter user email:")
    #     password = getpass("Enter user password:")
    #     app1name = input("Enter name of first WaaS app to compare:")

    # print("App1: " + app1name)
    # Show list of applications, and servers for each application
    apps = waas_api_get(token, 'applications')

    # Verify that each of these apps is present
    app1 = is_app_present(apps['results'], app1name)
    if app1:
        yay = True
    else:
        sys.exit("App1 (" + app1name + ") not found")

    # print("App id found: {}".format(app1))
    app1data = waas_api_get(token, "applications/" + str(app1) + "/")

    if pretty_print:
        print(json.dumps(app1data, indent=2))
    else:
        print(json.dumps(app1data))
