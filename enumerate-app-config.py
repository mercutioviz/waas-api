import requests
import pprint
import sys
from getpass import getpass
from urllib.parse import urlencode, urljoin
import json

API_BASE = "https://api.waas.barracudanetworks.com/v2/waasapi/"
config_items = ('advanced_threat_protection',
                'allow_deny_headers',
                'allow_deny_urls',
                'caching_and_compression',
                'clickjacking_protection',
                'cookie_security',
                'data_theft_protection/data_types',
                'data_theft_protection',
                'endpoints',
                'ip_reputation',
                'load_balancing',
                'log_server',
                'parameter_protection',
                #'profile_parameters',
                'request_limits',
                'request_rewrite',
                #'request_rewrite_rule',
                'request_rewrite_rules',
                'response_cloaking',
                'trusted_hosts',
                'trusted_hosts_group',
                'url_normalization',
                #'url_profile',
                'url_profiles',
                'url_protection',
                'virus_scanning'
                )

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
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        app1name = sys.argv[3]
    else:
        email = input("Enter user email:")
        password = getpass("Enter user password:")
        app1name = input("Enter name of first WaaS app to compare:")
    token = waas_api_login(email, password)

    #print("App1: " + app1name)
    # Show list of applications, and servers for each application
    apps = waas_api_get(token, 'applications')

    # Verify that each of these apps is present
    app1 = is_app_present(apps['results'], app1name)
    if app1:
        yay = True
    else:
        sys.exit("App1 (" + app1name + ") not found")

    #print("App id found: {}".format(app1))
    app1data = waas_api_get(token, "applications/" + str(app1) + "/")
    #print(json.dumps(app1data, indent=2))
    for item in config_items:
        # if item != 'ip_reputation':
        #     continue
        config_data = waas_api_get(token, "applications/" + str(app1) + "/" + item + '/')
        if config_data:
            print("Config info for " + item + ':')
            print(config_data)
            print()
        else:
            print("No config info for " + item)
            print()

    comp1data = waas_api_get(token, "applications/" + str(app1) + "/components/")
    print(json.dumps(comp1data,indent=2))