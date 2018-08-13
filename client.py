import httplib
import urllib
import json
import optparse

params = urllib.urlencode({'username': 'admin', 'password': 'iamadmin'})

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost", 8888)

conn.request("POST", "/", params, headers)
response = conn.getresponse()
key = json.loads(response.read())['key']


def menu(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    if arg['event'] == 'edit':
        params = urllib.urlencode({'key': key, 'item_name': arg['item_name'],
                                   'price': arg['price'],
                                   'category': arg['category'],
                                   'old_item_name': arg['old_item_name'],
                                   'event': arg['event']})
    else:
        params = urllib.urlencode({'key': key, 'item_name': arg['item_name'],
                                   'price': arg['price'],
                                   'category': arg['category'],
                                   'event': arg['event']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/menu", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def team(arg):

    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key, 'team_name': arg['team_name'],
                                   'event': arg['event']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/team", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())

if __name__ == '__main__':

    parser = optparse.OptionParser(usage="usage: %prog [options] filename",
                                   version="%prog 1.0")
    parser.add_option('-m', '--menu',
                      dest="menu",
                      help='add /update/ delete menu',)

    parser.add_option('-t', '--team',
                      dest="team",
                      help='add / delete team',)

    (options, args) = parser.parse_args()

    if options.menu:
        menu(options.menu)
    if options.team:
        team(options.team)
