# waas-api
Barracuda WaaS API examples

All script examples accept two or more CLI arguments (positional):
- Username
- Password
- App1 Name
- App2 Name

The scripts are described as follows:
compare-apps.py - WIP, to compare the JSON config dump of two apps
dump-apps.py - JSON pretty print dump of all apps found for the supplied creds
dump-waas-app.py - JSON pretty print dump of specified app
enumerate-app-config.py - WIP, makes multiple GET requests for all the APIs in the WaaS Swagger API docs
list-apps.py - Simple list of apps found for the supplied creds.
